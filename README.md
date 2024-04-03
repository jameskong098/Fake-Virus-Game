# COSI 107A Project Proposal - Phishing for a Trojan
## James Kong, Jeremy Bernstein, and Eric Hurchey

### Overview
We plan to research how computer viruses, phishing, and online scamming work. After researching how they work, we would like to see if we can make a “Trojan Horse” type program. There are many ways that online hackers can create fake websites, emails, links, and programs to trick innocent people who may not know better. Our goal is to look into the security of how it works, how applications can potentially bypass privileges and cause harm to a system, and figure out a potential delivery solution that could successfully disguise the delivery of the program. In general, we would like the program to be discreet and run malicious activity in the background while the foreground displays seemingly innocent/harmless activity.

Ideally, we plan to insert the trojan into the victim’s computer through a social engineering scheme using the tools available in Kali Linux, such as the Social Engineering Toolkit (SET). We plan on delivering the trojan through email or the internet under the guise of a legitimate application. However, the difficult portion of designing a social engineering scheme is to convince people with technological savviness and those who are woke to computer security. To overcome this challenge, we plan on designing a legitimate piece of software that contains malicious code that would allow us to monitor and maintain access to a compromised machine. The goal is to not only be able to convince the “usual targets,” but people in our demographic that can easily detect a potential security threat.

### Core Requirements
Some of the core requirements of this project would involve a successful executable program disguised as a normal program that performs malicious activity behind the scenes and a successful social engineering scheme to deliver our program to an unsuspecting user. In terms of how we would like to present it, we were thinking of making a video that we will edit and put together showcasing some background information on the topic along with a demonstration of how our application works along with the method of delivery. Jeremy has a great video editing background, so we plan to utilize that to put together a nice professional, and informative documentary-esque film. As for the program, we were thinking of coding in Python and utilizing many different libraries relating to the Operating System. We also need to see how to package Python files into Windows executables. If we go the route of a game, we might potentially use Unity as there is a Python Unity library but more research needs to be done. There are also a ton of Python libraries that are good for game development as well such as Pygame, PyKyra, Pyglet, and more. More information about the game route can be found below where we discuss potential ideas.

- One potential idea we have is to make some sort of program that looks like a funny troll game. We got this idea as sometimes we will see funny trending games such as Flappy Bird and want to download them and play them. The idea is that since the game looks simple and like a troll game, people will let their guard down thinking it's safe. 

- Another potential idea that we currently have includes mimicking an application such as a Zoom client, posing as an IT Staff member from Brandeis emailing about a ticket a client made about obtaining a certain Brandeis software. 

- Another potential idea is a scheduler, similar to When2Meet, that allows the user and other users they invite to create a shared calendar of each other’s availability on a software application with a high-quality UI.

### Beyond The Core Requirements
To improve the effectiveness and efficiency of our trojan application, we hope to develop a full software product that is convincing enough to be downloaded by a reasonable amount of users. We plan to utilize our software engineering background to develop an application that performs a legitimate function that would improve the user’s quality of life or offer an entertainment value. Once the software is complete, we intend to inject the malicious code deep within the codebase to avoid detection from modern web browsers or antivirus software such as Windows Defender or Malwarebytes. This will allow us to focus on the product which will maximize the potential to get as many downloads as possible, thus improving the reach of the malicious hack.

### Stretch Goal
Additionally, we would like to work with test subjects to verify the success of the social engineering tactics being devised for this exploit. In these experiments, we intend to utilize dummy versions of the program that do not contain any malicious code solely to verify the success of our social engineering tactics. Furthermore, an additional concern is how to allure potential testers without disclosing the reason for the test or that they are involved in some form of social experiment. The goal is to convince people neither of us are associated with to download what they believe to be a legitimate piece of software without any in-person influence. Similarly, we would like to develop an online API for our website that will allow the user to store information online in addition to within the software. This not only improves the efficiency of what the user believes to be valid software but also opens the door to a plethora of available exploits that can be used to gain more information on the victim. Lastly, we think it would be more engaging for the user to incorporate AI to some degree into our program via APIs.

### Research

- https://www.tutorialspoint.com/kali_linux/kali_linux_maintaining_access.html

- https://thepythoncorner.com/posts/2021-08-30-how-to-create-virus-python/

- https://oag.ca.gov/privacy/facts/online-privacy/protect-your-computer

- https://www.fortinet.com/resources/cyberglossary/trojan-horse-virus#:~:text=A%20Trojan%20Horse%20Virus%20is,system%20access%20with%20their%20software 

- https://www.kali.org/tools/set/ 

- https://helpdeskgeek.com/how-to/what-is-an-executable-file-how-to-create-one/

- https://www.advancedinstaller.com/create-setup-exe-visual-studio.html

- https://analyticsindiamag.com/top-9-python-frameworks-for-game-development/

- https://www.ursinaengine.org/

- https://yash7.medium.com/how-to-turn-your-python-script-into-an-executable-file-d64edb13c2d4#:~:text=PyInstaller%20is%20a%20Python%20library,Linux%2C%20and%20Mac%20OS%20X.