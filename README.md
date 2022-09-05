**TwitterCreationBot**<br />
 This bot's goal is to create twitter accounts using various email types. Unfortunately, twitter has added a capatcha verfication step to lessen the chance of making accoutns through bots. I tried countring that by training Yolov5s on images collected from twitter's website, but they ultimately changed the type of images and the model included with this code is no longer of use. In case you find a way to bypass the captcha, this bot will be of a great help for in making accounts and tweeting from them. 
 
 There are various email options to choose from. There is the TempMail API option, which requires you to have an api key from RapidAPI. There is also another great option, which is MinuteInbox, though your ip will probably get blocked if you make too many requests. There is also the option to use Hotmail(you can buy bulk hotmail through hotmailbox.net). Last but not least, you can also use gmail and using the dot trick you can make thousands of accounts with one email. This bot also has the option to use protonmail, but it is a really slow option as the bot creates the email account on spot while making the twitter account, and as it uses [hcaptcha-challenger](https://github.com/QIN2DIM/hcaptcha-challenger), using the browser in headless mode is not possible, add to that the performence overhead introduced by inference. To configure which email service you would like to use, you need to do it in the Twitter_temp.py, as this is the brain of the bot.
