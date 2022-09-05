# -*- coding: utf-8 -*-
# Time       : 2022/1/16 0:25
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import time
import warnings
from typing import Optional
import re
from selenium.common.exceptions import WebDriverException

from services.hcaptcha_challenger import ArmorCaptcha, ArmorUtils
from services.hcaptcha_challenger.exceptions import ChallengePassed
from services.settings import (
    logger,
    HCAPTCHA_DEMO_SITES,
    DIR_MODEL,
    DIR_CHALLENGE,
    PATH_OBJECTS_YAML,
    PATH_RAINBOW_YAML,
)
from services.utils import get_challenge_ctx

warnings.filterwarnings("ignore", category=DeprecationWarning)


@logger.catch()
def runner(
    sample_site: str,
    lang: Optional[str] = "zh",
    silence: Optional[bool] = False,
    onnx_prefix: Optional[str] = None,
    screenshot: Optional[bool] = False,
):
    """Human-Machine Challenge Demonstration | Top Interface"""

    # Instantiating Challenger Components
    challenger = ArmorCaptcha(
        dir_workspace=DIR_CHALLENGE,
        lang=lang,
        debug=True,
        dir_model=DIR_MODEL,
        onnx_prefix=onnx_prefix,
        screenshot=screenshot,
        path_objects_yaml=PATH_OBJECTS_YAML,
        path_rainbow_yaml=PATH_RAINBOW_YAML,
    )
    challenger_utils = ArmorUtils()

    # Instantiating the Challenger Drive
    ctx = get_challenge_ctx(silence=silence, lang=lang)
    _round = 5
    code = ''
    try:
        while not code:
            try:
                # Read the hCaptcha challenge test site
                ctx.get(sample_site)

                # Detects if a clickable `hcaptcha checkbox` appears on the current page.
                # The `sample site` must pop up the `checkbox`, where the flexible wait time defaults to 5s.
                # If the `checkbox` does not load in 5s, your network is in a bad state.
                if not challenger_utils.face_the_checkbox(ctx):
                    break

                start = time.time()

                # Enter iframe-checkbox --> Process hcaptcha checkbox --> Exit iframe-checkbox
                challenger.anti_checkbox(ctx)

                # Enter iframe-content --> process hcaptcha challenge --> exit iframe-content
                resp = challenger.anti_hcaptcha(ctx)
                if   resp == challenger.CHALLENGE_SUCCESS:
                    try:
                        ctx.switch_to.default_content()
                    except Exception as e:
                        print(e)
                    hcap=ctx.page_source
                    code = re.findall('data-hcaptcha-response="(.*)" style=',string=hcap)[0].split('"')[0]
                    break
                elif resp == challenger.CHALLENGE_RETRY:
                    ctx.refresh()
                    logger.error(f"RETRY[{1 + 1}|5]".center(28, "="))
                
            # Do not capture the `ChallengeReset` signal in the outermost layer.
            # In the demo project, we wanted the human challenge to pop up, not pass after processing the checkbox.
            # So when this happens, we reload the page to activate hcaptcha repeatedly.
            # But in your project, if you've passed the challenge by just handling the checkbox,
            # there's no need to refresh the page!
            except ChallengePassed:
                # ctx.refresh()
                try:
                    ctx.switch_to.default_content()
                except Exception as e:
                    print(e)
                hcap=ctx.page_source
                code = re.findall('data-hcaptcha-response="(.*)" style=',string=hcap)[0].split('"')[0]
                logger.success(f"PASS[{1 + 1}|5]".center(28, "="))
                break
            except WebDriverException as err:
                logger.exception(err)
    finally:
        # frame = ctx.find_element(By.XPATH,'/html/body/div[5]/form/fieldset/ul/li[2]/div/div/iframe')
        # ctx.switch_to.frame(frame)
        ctx.quit()
        return code
@logger.catch()
def test():
    """Check if the Challenger driver version is compatible"""
    ctx = get_challenge_ctx(silence=True)
    try:
        ctx.get(HCAPTCHA_DEMO_SITES[0])
    finally:
        ctx.quit()

    logger.success("The adaptation is successful")
