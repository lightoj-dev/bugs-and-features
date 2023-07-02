# LightOJ - Adding Problem and Contests

To arrange a contest on LightOJ the following steps would be required:



1. First login to the platform. Go to [https://www.lightoj.com](https://www.lightoj.com) and login. You can sign in using your gmail/github account and can skip registration completely.

To arrange a contest, you need to have a few problems. Problems and contests are separate entities, first we need to add problems onto the platform.


## Special Notice

Currently one can host contests for free on LightOJ which doesn’t include any live support or assurance that the LightOJ’s server will be available to serve. If you want to host a contest with more than 50 participants, or require special support from the LightOJ admin team, please reach us over [facebook messenger](https://m.me/lightoj) or create a ticket  [here](https://github.com/lightoj-dev/bugs-and-features/issues).


## Terms and Conditions

If you are using LightOJ’s problem creation and contest hosting tool, you are agreeing with LightOJ’s [terms of service](https://github.com/lightoj-dev/privacy-policy/blob/master/terms-of-service.md), and specially you should not try to exploit the system and use this tool to exploit the users of LightOJ. You can not create any content on LightOJ which can be used to insult or bully some person or a group. If you try to do so, we may ban you from the platform or even take legal action. If you are unsure about anything or need to learn more, please reach us over the [facebook messenger](https://m.me/lightoj) or create a ticket [here](https://github.com/lightoj-dev/bugs-and-features/issues).

## Privacy Notice for LightOJ

This Privacy Notice outlines how we collect, use, disclose, and protect personal information on lightoj. We are committed to ensuring the privacy and security of your personal information. Please read this notice carefully to understand our practices regarding your data.

**Collection of Personal Information:**

When you register for the programming competition, we may collect personal information such as your name, email address, username, and country of residence.
We may also collect additional information related to your participation in the competition, such as your submission history and competition results.
We collect this information to administer the competition, communicate with participants, and ensure fair competition.
Use of Personal Information:

We use the personal information provided during registration to verify your eligibility, communicate important updates about the competition, and provide competition-related services.
Your personal information may also be used to generate anonymous statistics and reports for internal analysis and improvement of our competition platform.

**Disclosure of Personal Information:**

We may share your personal information with trusted third-party service providers who assist us in operating the competition platform, such as hosting providers and email communication platforms. These third parties are obligated to maintain the confidentiality and security of your personal information.
We may disclose your personal information if required by law or in response to a valid legal request.
Data Security:

We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.
We restrict access to personal information to authorized personnel who need to know the information for competition administration purposes.
Data Retention:

We retain your personal information for as long as necessary to fulfill the purposes outlined in this Privacy Notice, or as required by law.
Your Rights:

You have the right to access, correct, or delete your personal information held by us. Please contact us using the information provided below to exercise these rights.
You have the right to withdraw your consent for the processing of your personal information. However, this may result in your disqualification from the competition.

**Links to External Websites:**

Our website may contain links to external websites. We are not responsible for the privacy practices or content of these websites. We encourage you to review the privacy policies of any external websites you visit.

**Updates to Privacy Notice:**

We may update this Privacy Notice from time to time to reflect changes in our privacy practices. The updated version will be posted on our website, and the date of the last revision will be indicated.
Contact Us:

If you have any questions, concerns, or requests regarding this Privacy Notice or the handling of your personal information, please contact us at admin@lightoj.com.

By participating in the programming competition and using our website, you acknowledge that you have read and understood this Privacy Notice and consent to the collection, use, and disclosure of your personal information as described herein.

## Account Deletion
Please send us an email at admin@lightoj.com if you want us to delete your information from the system. Please note that, this acion is not reversible, i.e once done all your personal information with submissions in the system will be deleted.

# Adding Problems

If you make any changes, make sure to hit the **Save** button.

1. Go to [https://lightoj.com/author](https://lightoj.com/author) and click **Problems** from the right nav.
2. On the top right, you can select **Create New Problem**.
3. Add problem title and handle (handle is unique across the system, letters numbers and dashes are allowed)
4. **Statements:** Add **Description** to state the problem, add **Input** and **Output** to describe the output format. If the problem statement has some theories, you might add notes (optional).
5. **General:**
    - **Problem title** and **Problem Handle** are there, you might be able to change it if needed.
    - **Problem Type** can be Algorithm or Database depending on if the problem is a traditional algorithmic problem, and it’s a sql problem.
    - **Problem Status** can be **in-progress**, once done can be changed to **done**.
    - **Is dataset open** should be set to **NO** (default).
    - **Short Description** can be left blank, or you can add one for future reference (optional).
6. **Dataset:**
    - Datasets are very important for a problem to verify correctness. Add sample.in and sample.out files. **sample.in** should contain a sample input for the problem which the contestants will see when they open the problem. Same goes for **sample.out** which contains the output for the sample.in.
    - You can add multiple samples, upload the dataset first, then click on edit dataset button, and check the _sample_ checkbox, then save the changes.
    - Add a few datasets, you can choose any name, but the only restriction is that the input and the output file name should be the same. If **a.in** is the input file name then the corresponding correct output should be in **a.out**. Other than samples, these files will be hidden to the contestants and lightoj will verify user solutions based on these files. Try not to add more than 20 files per problem (10 input and 10 output files.)
    - You need to set the “active” flag for all the datasets (even the sample datasets) you want to use during a contest. Upload the dataset first, then click on edit dataset button, and check the “active” checkbox, then save the changes.
    - For database problems, the input and output files need to be in a certain format. The editor should help you with that. Feel free to reach out if you need help.
7. **Limits:**
    - **Memory limit** defines how much memory the user solution is allowed to consume. Set 128 if unsure.
    - **Time limit** defines how much cpu the user solution is allowed to consume. Set 2 seconds if unsure.
    - **Accepted Programming Languages** can be left empty to allow all the available programming languages. If you want users to use only python, c++, then just select these two.
8. **Checker**: Use **default** for simplicity. If your output has floating point numbers, then use the **Float checker** type. Please contact us if you want to use a special judge.
9. **Permissions:** By default, only the author can view/edit the problem. If you want others to edit the problem, please add permission. 
10. **Solutions**: You can add solutions for the problem, you should run the solution and see how much memory and time the judge solution is taking. Based on that, adjust the problem time and memory limit. Selecting time and memory can be tricky based on the solutions. Feel free to reach out if you need help.
11. **Submissions**: Will show you the judge solutions you have run, just for bookkeeping.
12. **Solution Templates**: Completely optional, this will be loaded when a contestant opens the problem as part of the solution.
13. **Input Generators**: For now, ignore this.


# Adding Contests

1. Go to [https://lightoj.com/author](https://lightoj.com/author) and click **Contests** from the right nav.
2. Click **Create new contest**
    - **Contest Title** should be the name of the contest
    - **Contest handle** is unique across all contests, letters, numbers are dashes are allowed.
    - **Participation type** should be **individual**.
    - Set the contest start time and end time (This is based on your local time zone).
3. Click **Settings** from the right nav.
    - Add **contest description**, this will be visible to the contestants when they view the contest.
    - **Contest Announcement** will be notified to the contestants when the contest is running. If there is any error in the contest, or related to any problem statement, you can update in the announcement.
    - **Contest Type** should be icpc.
    - **Contest Participation** Type must be private.
    - For simplicity, keep the freeze time the same as end time.
4. Click **Problems** and Add Problems. Search for the problem you would like to add in this contest. You can add as many problems as you like (Maximum 26). For now keep the same score for all the problems. Problem search option will show both your created problems and the problems available on the volumes.
5. **Permissions**, if multiple people are arranging the contest, please add the authors. There are different roles, just use **judge** for now.
6. **Participants:** You have to add all the users (if invite only) here who will participate in the contest. Keep in mind that the contestants have to be registered on LightOJ.
7. **Submissions**: Will show all the submissions of the contestants.
8. **Clarifications:** Contestants can ask about clarifying questions, judges can see all the questions here and can answer as necessary. The reply page is self sufficient.
9. **Standings:** Shows the contestant rank list.
