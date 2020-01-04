

# Artifact Auction

[![Build Status](https://travis-ci.org/Shilldon/artifact-auction.svg?branch=master)](https://travis-ci.org/Shilldon/artifact-auction)

## UX Overview

### Brief
This website has been created as a tool to enable the site owner to earn money through auctioning and selling unqiue historical artifacts.
The site owner's brief requires that users can bid against artifacts or pay a higher price to purchase them immediately.

The objectives are:  
1 - Provide a site for the owner to upload and auction artifacts.  
2 - Enable users to:
  - Browse artifacts by various categories
  - Search for specific artifacts
  - Bid on and purchase artifacts
  - Learn more about the history of the artifacts on the site  

3 - Provide a visually appealing environment in keeping with the tone of the artifacts being auctioned.

### User Stories
There are two distinct user groups who will access the site:
- The site owner and (if applicable) staff who will need administrative access to upload artifacts and edit auctions; and
- Site users who will need to be able to search for, bid on and purchase artifacts.

To that end user stories have been considered for both these groups.  
#### As the site owner:
- I want to upload details (price, description, historical information) of artifacts to the site
- I want to set up auctions to sell the artifacts
- I want to set up auctions to start in the future
- I want to be able to set reserve prices on artifacts so they cannot be sold for less than the reserve
- I want to see what bids users have placed on the artifacts
- I want to give users the option to buy artifacts immediately
- I want to educate users on the history of artifacts
- I want to show artifacts that are not in auctions
- I want to show artifacts have have been sold
- I want users to encourage users to place more bids
- I want to see and edit reviews left by users who have purchased artifacts
- I want to prevent users reviewing artifacts they do not own

#### As a potential purchaser and bidder:
- I want to find a particular artifact
- I want to search for artifacts of a particular type
- I want to leave a review of an artifact
- I want to see who currently owns an artifact
- I want to find out what historical figures of note owned an artifact
- I want to see all auctions that are currently live
- I want to find all artifacts that are in live auctions
- I want to find all artifacts that have been sold
- I want to find all artifacts that have not, yet, been sold
- I want to bid in an auction
- I want to purchase an artifact immediately.
- I want to see who else has bid on an artifact and the amount they bid
- I do not want other users knowing what artifacts I have purchased
- I do not want other users knowing what bids I have placed
- I want to see all artifacts I have purchased
- I want to see all artifacts I have won
- I want to learn about the history of an artifact

### Purpose and site overview
This website is designed as an interactive full stack site with a simple interface to enable users and the site owner to easily navigate around the site and achieve their aims, above.

#### Colour scheme and typography
The blue/gold colour scheme was chosen to reflect a sense of reliability and value of the artifacts being auctioned on the site. 

Blue is often associated with cultural and religious traditions and, as such, compliments the nature of many of the artifacts for sale on the site. 

Gold is typically associated with wealth, instilling a sense of value and priceless nature to the artifacts listed.

The company 'Jones & Son' has traditional values and has been established for many years. *Cinzel Decorative* font was chosen for the logo to reflect the sense of establishment and age of the company. 

*Montserrat* as a strong easy to read font was chosen for the main content.

#### Technology overview
The technologies used are further set out below, in brief,  the ***Django*** framework was used for user authentication and site administration.
The site owner, using the ***Django*** admin panel can add and edit models for artifacts, auctions, historical events and historical figures. Full instructions for site admin are contained in a modal through the *Admin Help* tab in the navbar if logged in as a superuser.

The models are stored in ***PostgreSQL*** database and accessed via ***Python*** backend code and the ***Django*** admin panel.

#### Navigation
The main navigation menu for the site is displayed at the top of every page or behind a burger button on smaller screens. The navigation options displayed are dependent upon the status of the user accessing the site:  
- Superuser
-- View artifacts, view collection, admin panel, admin help, profile and logout
- User logged in
-- View artifacts, view collection, profile, logout
- User not logged in
-- View artifacts, register/login

Removing options for users depending on their authority avoids confusion and provides a better user experience.
On smaller devices clicking the burger button will bring up a modal of menu options, as above. In addition to reduce the 'number of clicks' search and login/logout options are available through the relevant icons next to the burger button.

#### Website Layout
The site comprises 17 pages and a website map is contained in the repository. See *Website Layout* document in the *Design* folder in the repository for further information.
All pages are rendered using the ***Django*** backend framework, ***Jinja*** templating logic and ***HTML5***.

##### Base Template
All pages are served with a base template that provides:
- Navbar with menu links, as identified above
- Footer with links to a contact form and terms of use
- Back button to return to previous page (except on index page)

##### Index Page
This page provides an overview of the site and background to its purpose. On the desktop site there is an image link to a list of all the artifacts listed on the site and a carousel displaying images of the artifacts in currently live auctions (these images link directly to the relevant artifact). On smaller screens images and the carousel are omitted for better user experience simply providing a styled list of the artifacts in live auctions.

##### List of Artifacts Page
On initial view this page displays a complete paginated list of all artifacts on the site (pagination allows a maximum of 10 items per page). ***Django*** templating and ***Jinja 2.0*** are used to populate the page data.
Each artifact is displayed with:
- a thumbnail image (or a placeholder image if the admin user has not uploaded an image of the artifact); 
- a sold image superimposed on the artifact image if the artifact has sold;
- the name of the artifact; 
- ownership status (whether the artifact is owned and, if the owner has not chosen to remain anonymous, their first name - with a link to their profile);
- status of the auction ("Not yet listed for auction", "Time to start of auction", "Time left in auction", or "Auction finished").  

For artifacts in auctions that are pending or live a timer is displayed that is updated via ***jQuery*** polling.
The display of the sold and auction 'statuses' are determined by by a combination of ***Django*** templating and ***jQuery***.

The list of artifacts can be filtered and sorted through the three options at the top of the page:
- Search bar - a list of artifacts whose names contain the searched terms will be returned;
- Filter - brings up a modal with more detailed search options (Name, Description, Sold, Listed for Auction, Type, Category and Price);
- Sort - brings up a modal enabling the user to sort the returned results alphabetically or by price.

Filtered search and sorted results are returned via ***Python*** backend code.
The detailed filter options have been considered against user stories to ensure users are easily able locate specific artifacts or groups of artifacts.

##### Single Artifact Page
On selecting a specific artifact this page is rendered which provides details of the artifact selected using data from the backend Artifact model:
- Artifact image (if one has been provided by site admin, if not the page layout, using ***Bootstrap*** and ***Django*** templating is adjusted);
- About - information about the artifact which is set out in full on displays wider than 1024px but contained within a collapsible section on smaller screens;
- Ownership status - as above, if the artifact has been purchased the first name of the owner is displayed with a link to their profile (unless the user has chosen to remain anonymous);
- Auction status - if the artifact has not been sold the auction status is shown (with countdown timer), as above;
- Bid button - if the artifact is in a live auction and the user is logged in this button is displayed with a simple form to accept the value which the user wishes to bid;
- Buy Now button - if the artifact is in a live auction, the user is logged in and the site admin has given a buy now price for the artifact this button is displayed enabling the user to purchase the artifact immediately. As bidding increases the buy now price also increases so that it always exceeds the highest bid by 20% (this is achieved through updates to the artifact model in the backend).
- Bid History - if the artifact is in a live auction and at least one bid has been made on the artifact this link displays a modal listing the time, amount and user name (and link to their profile) of all bids made. (If users have chosen to remain anonymous their first names are not displayed, being replaced with 'anonymous' instead).

The following sections are dependent on the data associated with the artifact model and will not be displayed in all cases.
- Review - Where an artifact has been purchased and the owner is viewing the artifact they will be presented with an option to leave a review for the artifact. If they have done so all users will be able to view the review in the collapsible section and see the rating associated with the review.
- History - If an artifact has historical events associated with it (as input by the site admin) a list of these events in chronological order is displayed in a collapsible section. Each row in the list contains a link to a page detailing the event further and a link to the historical figure associated with that event.
- Historical Figures - If the artifact has historical figures associated with it (as input by the site admin) a list of these people is displayed in a collapsible section. Each row in the list contains a link to a page detailing the person further.

##### Add/Edit Review
This page is only available to a user who is logged in and has purchased the specific artifact. The user can complete a form setting out their review of the artifact. In addition they can rate the artifact on a scale of 0 to 5 by clicking on the relevant number of stars.
If there is already a Review model associated with this artifact the form is pre-populated with the data from that model otherwise a blank form is rendered.
The star selection is animated by ***jQuery*** and ***CSS*** and ***jQuery*** is used to update the integer value of the rating for the form for passing to the back end to create a new or update an existing Review model.
On this page the user also has the option of deleting an existing review.

##### Historical Event
On selecting a specific historical event this page is rendered using the ***Django*** framework and templating rendering data from the Event model.
The page has a similar layout to the artifact page to keep consistency across the site. If the site admin has uploaded an image in the Event model this is shown otherwise the page layout is adjusted using the ***Django*** templating and ***Bootstrap*** framework.
Information about the artifact is displayed and, if the text contains the name of the artifact and/or historical figure associated with the artifact these are converted to links to the artifact/historical figure's relevant page. (This conversion is undertaken when the Event model is saved).
Below the main information about the artifact a list of other events associated with this artifact is displayed under a collapsible in chronological order. Each row contains a link to the relevant event and, if applicable, the historical figure associated with that event.

##### Historical Figure
On selecting a specific historical figure this page is rendered using the ***Django*** framework and templating rendering data from the Historical Figure model.
In keeping with consistency across the site this page has the same layout to the Historical Event page, above, similarly adjusting if an image is not provided.
Links within the main information to the specific artifact are rendered in the same way as above.
Below the main information is are lists of the events with which the historical figure is associated and the artifacts with which they are associated as well. Both lists are contained within collapsibles and contain links to the relevant events and artifacts.

##### Collection Page
This page is similar in layout to the list of artifacts but displaying, instead, lists of artifacts the user has won but not, yet, paid for and artifacts the user has purchased.
If the user has artifacts in both categories a page breaker is displayed between the lists to make it clear to the user that they are different.
Where the user has artifacts pending purchase a total price for the artifacts is displayed along with a link to the checkout to enable the user to pay.
Pagination is applied to the list of artifacts purchased by the user (a limit of 10 per page) but not to the list of items won as due to the nature of the auctions this list is very unlikely to reach a significant number of items.

##### Checkout
On selecting the Buy Now option from the artifact page or Pay Now from the collection page this checkout page is rendered.
A list of the items the user is purchasing is displayed. This will only ever be one item where the user is using Buy Now to purchase an artifact in an auction but may be more than one item if the user has won more than one auction and has not immediately paid for the artifacts won.
The individual and total prices of the artifacts are displayed (calculated in the back end).
On selecting the Pay Now option a modal is displayed for the user to complete their personal and payment information.


The ***Stripe API*** is used to validate and submit payment information. The ***Stripe API*** key is contained within the page as a hidden element for accessing by the standard ***Stripe API*** ***jQuery*** payment processing code. If payment is successful, a success message is displayed and email sent to the user confirming their purchase and they are returned to their collection of artifacts.
If the payment is unsuccessful an error message is displayed and the payment modal remains.

##### User Account Pages
Within this category there are 7 pages relating to registration/login options and the user's profile.

##### View Profile
From the main navigation this page displays the user's profile:
- Profile picture; 
- Name;
- Username;
- Email;
- Bio

From this page the user can follow a link to edit their profile.
This page is alternatively displayed on clicking a link for another user's profile from the artifacts list or display artifact pages. Naturally the edit profile link is not provided in that case and the information provided is restricted to the user's name, profile picture and bio (their email address and username are hidden for security purposes).

##### Edit Profile
This page renders a form enabling the user to update all aspects of their profile. The form is pre-populated with data from the User model.
A 'change password' link is also displayed. See further, below (forgotten password under Login Page).
If the user has uploaded a profile picture this is displayed with the options to remove the picture or upload a new one.
Where a user opts to remove the picture ***jQuery*** is used to hide the picture and update the onscreen instructions on next steps.
Wher a user opts to change their picture ***jQuery*** is used to hide the original picture, display the name of the new picture selected to upload and update instructions on next steps.
Finally the user can amend their 'remain anonymous' status (a boolean value).
On clicking the "update" button at the bottom of the page the form is submitted to the backend and changes are saved to the User model.

##### Registration
The link to this page is only available if a user is not logged in. This page renders a form that is, in essence, identical to the edit profile form except it is not pre-populated with the user's data.
A profile picture is not displayed on this view.
On clicking the *register* button at the bottom of the page the form is submitted to the backend and a new User model is created.

##### Log In
The link to this page is only available if a user is not logged in. This page renders the ***Django*** framework user login form that is styled in keeping with the site.
A *forgot password* link is provided to enable users who have forgotten their password to change it.

##### Password Reset
This page renders the ***Django*** framework password reset form that is styled in keeping with the site. The user is prompted to enter their email address in order to reset their password.
On submission of this form if the entered email address is associated with a User model the user is emailed a link to the password reset confirm page with a form to change their password.

##### Password Reset Done
This page renders the ***Django*** framework confirmation that the request to reset the user's password has been received and an email sent to the user with instructions on next steps (the link referred to above).

##### Password Reset Confirm
This page renders the ***Django*** framework password reset confirm form that is styled in keeping with the site.  This page is accessed via the link emailed to the user, above.
This form prompts the user to enter their new password twice for validation. On successful submission of a new password the User model is updated with the new password.

##### Password Reset Complete
This page renders the ***Django*** framework confirmation that the user's password has been reset styled in keeping with the site and they are returned to the login in page.

### How does it work?

#### Data processing and entry
All data (users, artifacts, auctions etc.) is entered in the front end forms either on the main site by users creating their profiles or on the admin site by site admin using the standard ***Django*** admin panel. Data is primarily backend validated within the ***Django*** models and/or forms. If valid the data is submitted to the remotely hosted ***postgreSQL*** database.
***Python***/***Django*** is used to retrieve, filter and sort data from the data tables and pass to front end for display.

#### Database Structure
Conceptual database design was undertaken considering the entities, their relationships and attributes.   See *Conceptual Database Design* and *Data Relationships* documents in the repository.
User data is limited to data required to enable the user to log on and identify themselves.
Artifact data is much broader containing data about the artifact (price, owner, sale price, description etc.) and background information about the artifact (historical events, owners). 
It was decided that a relational database structure was appropriate to avoid data duplication, provide security (the site admin would be the only user able to edit and update artifact data) and the flexibility to query what could potentially be a large database of users and artifacts.
From the conceptual design data tables were drafted (see *Data Tables* document in repository) and ***Django*** models created from those tables.

#### Adding artifacts and auctions
Full instructions for site admin to add artifacts and auctions to the site can be found in the *Site Admin* tab if logged in as a superuser.

In brief site admin can interact with the database and add models using the ***Django*** admin panel. While site admin can create custom categories (with descriptions) for artifacts all artifacts may only belong to one type as specified by archaeological convention:
- Historical and cultural
- Media
- Knowledge
- Data

The ***Django*** artifact model is, therefore restricted in this manner.

#### Bidding

Site admin may set reserve and buy now prices for artifacts.

##### Reserve price

The function of the reserve price is to enable site admin to specify the minimum amount for which they would like the artifact to sell. Users are informed if there is a reserve price set on the artifact but are not made aware of the actual reserve otherwise this would affect bidding.

Users will still have the option to purchase artifacts with a reserve immediately. In the on site guidance the admin is encouraged to set the buy now price suitably higher than the reserve and form validation ensures the buy now price (if given) cannot be set lower than the reserve price.

##### Buy now price

Site admin can set the initial buy now price on the Artifact Model. If set this is the price for which users can immediately purchase the artifact irrespective of current bidding.

If, at any stage, the current highest bid exceeds the buy now price and the reserve price the buy now price value on the Artifact Model is updated to 20% more than the current highest bid.

This increase is designed to encourage users to continue to place bids on the artifact while, at the same time, allowing users to opt to immediately purchase the artifact albeit for more than the current bid.

An artifact may not, necessarily, have a reserve and a buy now price. If the buy now price is not set on the artifact model the user will not have the option to purchase the artifact immediately until bidding exceeds the reserve price at which point the buy now price will be set at 20% more than the highest bid.

##### Bidding process

Users may bid on artifacts by submitting an amount through the Bid Form on the *Single Artifact* page.

The current highest bid is retrieved from the Bid Models associated with the relevant auction. If the bid value entered by the user is higher then another Bid Model is created for the new bid.

The bid value is also compared to the reserve and buy now prices (if any) for the specific artifact. If higher than both the reserve and buy now the buy now price on the artifact is updated to 20% more than the current buy now price.

The user will then not have a buy now option for the relevant artifact until another user places a bid. This is to prevent abuse and artificial price increases by users.

### Features

#### Existing Features
 - Users can register for accounts to enable them to bid on artifacts
 - Users can upload unique profile pictures
 - Users can change their profile details (e.g. name, email address and/or profile picture, bio)
 - Artifacts on the site can be browsed and searched by different attributes:
    - Name
    - Description contents
    - Sold/Unsold status
    - Listed/Not listed for auction status 
    - Custom artifact categories (e.g. weapon, mechanism etc.)
    - Artifact type (Cultural, Media, Knowledge or Data)
    - Maximum and/or minimum purchase price
 - Currently live auctions are displayed on the homepage with links to those auctions
 - Site admin can provide background information for the artifacts including:
    - Events that took place in the artifact's history
    - Details of individuals associated with the artifact during its history
 - Bidding system implemented using ***jQuery*** polling that updates the page to display the current bid
 - A 'buy now' option to enable users to end an auction early by purchasing an artifact for an enhanced price
 - An optional 'reserve' price is available to site admin to prevent artifacts from selling for less than a specified price
 - Paginated display for lists of artifacts (on the site or owned by the user) that exceed 10 artifacts in length
 - Responsive design for best view on various device sizes
 - Collapsible headers and body for historical information about artifacts to provide better read format
 - Option for users to add a written review and 5-star review rating after purchasing an artifact
 - Option for user information to be kept anonymous so it is not evident to other user's that they have bid or own particular artifacts
 - Usernames and email addresses are hidden from view for other users for security purposes
 - Users can view a list of all artifacts that they own or have won in auctions
 - Site admin can access the Django Admin Panel which provides many additional features such as creating artifacts, auctions, details of historical events and figures. These options are not available to other users.
 - All areas of the site can be navigated from the main menu which is customised depending on the status of the user (logged in, admin or logged out)
 - Automated emails sent to bidders to inform them when they are outbid on artifacts

#### Features left to implement

- Currently it is necessary for site admin to contact a user on the end of an auction to inform them that they have won an artifact and to request payment. Ideally this process could be automated in the back end through staged or timed background events. This could be achieved through task queue implementation using ***Celery***.

- Users are only aware of new auctions by accessing the site. A helpful feature would be an automated email sent to all registered users of the site to inform them of a new auction and the start date. It would be possible for users to set email preferences so that they are only emailed about specific types of artifact, if they so desire.

- Users cannot delete their own accounts and it is necessary for this to be undertaken by site admin.

#### Defensive design
Where possible options have been limited to prevent users from entering invalid data:
- ***Django*** admin panel uses backend form validation to ensure data entered is in the correct format
- Custom ***Django*** validation is used for specific data such as auction start and end dates to ensure the start date is not set after the end date
- ***jQuery*** in conjunction with front end ***HTML*** form validation is used to ensure correctly formatted data is provided on creating a profile
- ***Python*** back end validation is used to ensure bids entered are valid and higher than previous bids

### Deployment
The Artifact Auction website is deployed using the ***Heroku*** platform and can be viewed [here](https://shilldons-artifactauction.herokuapp.com/)

#### Deployment and integration process undertaken
The following sets out an overview of the deployment and integration process followed during development of the app. Instructions to deploy locally and remotely can be found thereafter.
The app and all associated files were developed through ***AWS Cloud9 IDE***.
A git respository was created through the bash terminal and the the project was committed to the repository using the standard bash commit command.
Commits to the respository were made at each major development stage or as issues were identified and fixed.

The project was then deployed to ***Heroku*** on the master branch through the ***Heroku*** online console, using the following steps:
- Having logged into the ***Heroku*** platform a new app was created, titled 'shilldons-artifactauction'.
- A git url was provided by ***Heroku*** on creating the app, 'https://git.heroku.com/shilldons-artifactauction.git'
- The local git respository was linked to ***Heroku*** through the bash terminal command
  ```
  git remote add heroku https://git.heroku.com/shilldons-artifactauction.git
  ```
- Using the ***Heroku*** dashboard the ***Heroku Postgres*** 'add-on' was attached 
- A requirements.txt file was created through the bash terminal command 
  ```
  sudo pip3 freeze --local>requirements.txt
  ```
- The requirements.txt file was commited to the local git repository
- A Procfile was created by bash terminal command
  ```
  echo web: gunicorn artifact_auction.wsgi:application > Procfile
  ```
- The Procfile was commited to the local git respository
- The local git repository was deployed to ***Heroku*** via the bash terminal command
  ```
  git push heroku master
  ```
- A user account for ***Stripe API*** was created using the online dashboard at [Stripe](https://stripe.com/gb) 
- ***Stripe API*** secret and publishable keys were generated for the account for use in the code
- A specific *gmail* email address was created using the online [Gmail dashboard](https://gmail.com) 
- Email host, transfer protocol and port details were obtained and included in *settings.py* 
- Local environment variables for:

    AWS_ACCESS_KEY_ID,

    AWS_SECRET_ACCESS_KEY,
    
    DATABASE_URL,
    
    DISABLE_COLLECTSTATIC,
    
    EMAIL_ADDRESS,
    
    EMAIL_PASSWORD,
    
    SECRET_KEY,
    
    STRIPE_PUBLISHABLE, and
    
    STRIPE_SECRET
        
were set using the ***Heroku*** console. (During development these variables were contained in a local *.env* file)
The local git repository was also pushed to ***GitHub***:

The project was then deployed to ***GitHub***:
- A repository titled "artifact-auction" was created in ***GitHub***.
- A URL was supplied by ***GitHub*** "https://github.com/Shilldon/artifact-auction.git"
- The remote repository was linked to the local git repository through the bash command
  ```
  git remote add origin https://github.com/Shilldon/artifact-auction.git
  ```
- The local repository was pushed to the remote repository using bash command
  ```
  git push -u origin master
  ```

The ***GitHub*** and ***Heroku*** repositories were linked using the ***Heroku*** console tab *Deploy* and selecting the option to connect to ***GitHub***.

The ***GitHub*** artifact auction respository was located and linked to ***Heroku*** and the option for automatic deploys selected to ensure the code pushed to ***GitHub*** matched the build on the ***Heroku*** platform. 
Automatic deployment to ***Heroku*** ensures app is built from the latest code pushed to the ***GitHub*** repository.

Static files are hosted using ***Amazon AWS S3***. Instructions are set out below to create an account to host static files to ***Amazon AWS S3***

There are no differences between the development and deployed versions.

Other than a standard browser no further software or implementation is required and the site can be accessed [here](https://milestone-3-recipebook.herokuapp.com/).

To test and run the ***Python*** code locally it is necessary to ensure all relevant requirements are installed locally. (Please see *requirements.txt* for the required libraries.)

#### Local Deployment
To edit and run the app locally the following are required:
- Development IDE (VSCode or similar)
- Python3 to run the app
- GIT to pull code and version control
- PIP for requirement installation

To edit/run the code locally it is necessary to clone the code from the ***Heroku*** or ***GitHub*** repository. However, as the ***Heroku*** repository is intended for deployment purposes only it is recommended that the code is cloned from and pushed to the ***GitHub*** repository.

##### Steps
- To clone from the ***GitHub*** repository using bash:
	```
    $ git: clone https://github.com/Shilldon/artifact-auction.git
    ```
or
- Select the "Clone or Download" button from the git repository to download the app as a zip-file.
- Alternatively to clone from ***Heroku*** using bash:
	```
    $ heroku git: clone -a shilldons-artifactauction
	$ cd shilldons-artifactauction 
	```

- Create a *.env* file with the following credentials:<br>
    AWS_ACCESS_KEY_ID<br>
    AWS_SECRET_ACCESS_KEY<br>
    DATABASE_URL<br>
    DISABLE_COLLECTSTATIC<br>
    EMAIL_ADDRESS<br>
    EMAIL_PASSWORD<br>
    SECRET_KEY<br>
    STRIPE_PUBLISHABLE<br>
    STRIPE_SECRET<br>
    *(AWS KEYS are only required if you are hosting static files remotely using Amazon S3 Bucket)*
    *(STRPE KEYS are only required if using the ***Stripe API*** to handle payment)*
- Install requirements from requirements.txt using bash:
    ```
    $ sudo -H pip3 -r requirements.txt
    ```
- To run the app use the following bash command:
	```
	$ python3 manage.py runserver
    ```
- The IDE will provide a URL to the local ***Django*** server. Select that link or copy and paste into a browser window.
- A local SQL database will be created on running the app initially and contained in *db.sqlite3*
- All models must be migrated to the database using bash commands:

    ```
	$ python3 manage.py makemigrations 
	$ python3 manage.py migrate
	```
- Create a superuser account to access the ***Django*** admin panel by terminal command:
	```
    $ python3 manage.py createsuperuser
    ```
    
To use the ***Stripe API*** to handle card payments:
- Create an account through the [Stripe Console](https://stripe.com/)
- Navigate to *API Keys* where you will find two keys, a publishable key and a secret key. Both keys must be added to the *.env* file (above).

#### Remote Deployment
The app is deployed on ***Heroku*** using the master branch on ***GitHub***. To deploy remotely on ***Heroku*** follow the steps above to set up the app locally then:
- Create a requirements.txt file using bash command:
	```
	$ sudo pip3 freeze --local > requirements.txt
	```
- Create a Procfile using bash command:
	```
    $ echo web: gunicorn artifact_auction.wsgi:application > Procfile
    ```
- Create a ***Heroku*** account through the [Heroku Dashboard](https://dashboard.heroku.com/login)
- Create the project app using a unique name. Any name can be chosen but it is advisable to select a name specific to the app.
- Navigate to the *Deploy* tab and select *Connect Github* under *Deployment Method*.
- Select *Enable Automatic Deployment* which will ensure that, as files are pushed to ***GitHub*** they will be automatically deployed and updated to the app.
- To enable database hosting navigate to the *Resources* tab and under *Add-Ons* search and select *Heroku Postgres*.
- Make a note of the database url detail and add this to the configuration variables.
- Follow the steps above to create migrations for the ***postgres*** database and create a new superuser. 
Changes can then be to the cloned code and deployed to Github using bash commands:
```
$ git add .
$ git commit -m "commit message"
$ git push -u origin master
```
or
If deploying directly to ***Heroku*** use bash commands:
```
$ git add .
$ git commit -m "commit message"
$ git push heroku master
```
(NB git add . stages all code for committing. Individual files can be staged by bash
```
$ git add "filename and path"
```

To host static files remotely:
- Create an account at [Amazon AWS](https://aws.amazon.com/s3/)
- Create a unique S3 bucket from the S3 tab by selecting "create bucket"
- The bucket must have a unique name and it is advisable to select a name specific to the app. Keep a note of this name as it must be specified in the AWS Bucket policy, below.
- The configuration options do not need to be changed and the default options are acceptable.
- It is necessary to change the S3 bucket permissions:
- Navigate to "CORS configuration" and enter the following configuration:

```HTML5
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>HEAD</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <AllowedHeader>Authorization</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```
- Once done navigate to *Bucket Policy* and enter the following policy, replacing <***> with the AWS bucket name you specified, above:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<***>/*"
        }
    ]
}
```

- Once done navigate to [AWS IAM](https://console.aws.amazon.com/iam/)
    - Create a *New Group* selecting your S3 Bucket
    - Create a *New Policy* and *New User* and associate these to the group.

- With the S3 Bucket in place you can push static files to the AWS S3 Bucket using the bash command:

```
$python manage.py collectstatic
```
### Validation
* CSS
    * jigsaw.w3.org was used for validation of css code and did not generate significant errors
* HTML
    * validator.w3.org was used for validation of HTML code. Errors were thrown on the raw HTML code by the use of ***Jinja2*** templating language which was not recognised by the validator.
    * Validation was peformed a second time on the code rendered on site by copy and pasting from the 'view source' right click menu option.
* jQuery
    * codebeautify.org/jsvalidate and jshint.com/ were used for validation of ***jQuery*** code. No significant errors were generated.
* Python
    * pep8online.com was used to validate ***Python*** code and did not generate any errors.

### Technologies used

#### Development
- ***AWS Cloud9*** - IDE for development
- ***GitHub*** - project repository
- ***Heroku*** - project deployment
- ***MarvelApp*** - wireframe sketches

#### Front End
- ***HTML5*** - Base markup
- ***CSS3*** - Base cascading style sheets
- ***jQuery 3.4.1*** - javascript functionality for front end interaction and polling
- ***Bootstrap 4.0*** - layout and design
- ***Stripe API*** - payment processing
- ***Amazon AWS S3*** - static hosting
- ***Jinja2.0*** - rendering and template logic

#### Back End
- ***Python 3.6.8*** - Back-end programming language
- ***Django 1.11.24*** - Python web framework
- ***PostgreSQL 11.4*** - Relational SQL database

#### Icons
- ***Fontawesome 5.10.2*** - Icons

#### Fonts
- ***Google Fonts***
    - Cinzel Decorative - Main logo
    - Montserrat - Default font

### Testing
See additional README document for specific testing undertaken. 

### Initial Wireframes
Wireframes were designed using ***MarvelApp*** and can be located [here](https://marvelapp.com/project/4427911/)

## Credits:

### Code

Accounts and Checkout app based on and adapted from ***CodeInstitute*** Authentication and Authorisation module - Full Stack Web Developer Diploma - [Original Code](https://github.com/Code-Institute-Solutions/AuthenticationAndAuthorisation/tree/master/07-CustomAuthentication/01-email_authentication)

### Images

#### Site Images
[Menu link 'Artifacts'](https://pixabay.com/photos/temple-burma-wall-stone-figurines-195929/)  - Licence: CC0licence Public Domain

[Menu link 'Auction Gavel'](https://pixabay.com/photos/justice-court-hammer-auction-law-510742/) - Licence: [Pixabay Licence](https://pixabay.com/service/license/)

[Sold](https://pixabay.com/illustrations/stamp-sold-business-promotion-1726355/) - Licence: [Pixabay Licence](https://pixabay.com/service/license/)

[Default Profile Picture](https://pixabay.com/vectors/blank-profile-picture-mystery-man-973460/) - Licence: [Pixabay Licence](https://pixabay.com/service/license/)

[Admin profile picture](https://www.flickr.com/photos/30564364@N02/8830100398) - Licence: [Creative Commons Attribution 2.0 Generic License](https://creativecommons.org/licenses/by/2.0/deed.en)

[Atlas Background](https://www.flickr.com/photos/photoshoproadmap/7564204504) - Licence: [Creative Commons Attribution 2.0 Generic License](https://creativecommons.org/licenses/by/2.0/deed.en)

#### Artifacts
[Ark of covenant](https://commons.wikimedia.org/wiki/File:Royal_Arch_Room_Ark_replica_2.jpg) - Licence:  [Creative Commons Attribution-Share Alike 2.5 Generic Licence](https://creativecommons.org/licenses/by-sa/2.5/deed.en) - Photo by Ben Schumin

[Excalibur](https://pxhere.com/en/photo/1091249) - Licence: Public Domain

[Antikythera Mechanism](https://commons.wikimedia.org/wiki/File:The_Antikythera_Mechanism_(3471161471).jpg) - Licence: [Creative Commons Attribution 2.0 Generic License](https://creativecommons.org/licenses/by/2.0/deed.en) - Photo by Marcus Cyron

[Dead Sea Scrolls](https://en.wikipedia.org/wiki/Dead_Sea_Scrolls#/media/File:Psalms_Scroll.jpg) - Licence: Public Domain

[Mask of Tutankhamun](https://en.wikipedia.org/wiki/Tutankhamun#/media/File:CairoEgMuseumTaaMaskMostlyPhotographed.jpg) - Licence: [Creative Commons Attribution-Share Alike 3.0 Unported Licence](https://creativecommons.org/licenses/by-sa/3.0/deed.en)

[Stonehenge](https://pixabay.com/photos/stonehenge-england-vikings-picts-3649724/) - Licence: [Pixabay Licence](https://pixabay.com/service/license/)

[Rosetta Stone](https://en.wikipedia.org/wiki/Rosetta_Stone#/media/File:Rosetta_Stone.JPG) - Licence: [Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)

[Spear of Lugh](https://hu.wikipedia.org/wiki/L%C3%A1ndzsa) - Licence: [GNU Free Documentation License](https://en.wikipedia.org/wiki/Wikipedia:Text_of_the_GNU_Free_Documentation_License) - Photo by René Hanke

[Holy Grail](https://www.flickr.com/photos/spiritual_marketplace/2207966935) - Licence: [Creative Commons Attribution 2.0 Generic License](https://creativecommons.org/licenses/by/2.0/deed.en)

#### Historical Figure Images
[King Arthur](https://commons.wikimedia.org/wiki/Category:King_Arthur_in_art#/media/File:Charles_Ernest_Butler_-_King_Arthur.jpg) - Licence: Public Domain

[Moses](https://commons.wikimedia.org/wiki/File:Rembrandt_-_Moses_with_the_Ten_Commandments_-_Google_Art_Project.jpg) - Licence: Public Domain

[Indiana Jones](https://indianajones.fandom.com/wiki/Indiana_Jones) - Licence: [Creative Commons Attribution-Share Alike 3.0 Unported Licence](https://creativecommons.org/licenses/by-sa/3.0/deed.en)

[Professor de Solla](https://en.wikipedia.org/wiki/Antikythera_mechanism#/media/File:DerekdeSollaPrice.jpg) - Licence: Public Domain

[Lugh](https://commons.wikimedia.org/wiki/File:Myths_and_legends;_the_Celtic_race_(1910)_(14780314441).jpg) - Licence: [Flickr](https://www.flickr.com/commons/usage/)

[Spinal Tap](https://en.wikipedia.org/wiki/This_Is_Spinal_Tap#/media/File:Thisisspinaltapposter.jpg) - Licence: [FairUse](https://en.wikipedia.org/wiki/Fair_use)

#### Historical Events
[Death of King Arthur](https://commons.wikimedia.org/wiki/File:Battle_Between_King_Arthur_and_Sir_Mordred_-_William_Hatherell.jpg) - Licence: Public Domain

[Building of the ark](https://commons.wikimedia.org/wiki/File:The_Phillip_Medhurst_Picture_Torah_472._Building_the_ark_of_the_covenant._Exodus_cap_37._Mortier.jpg) - Licence: [Creative Commons Attribution-Share Alike 3.0 Unported Licence](https://creativecommons.org/licenses/by-sa/3.0/deed.en)

[Sword In the Stone](https://pxhere.com/en/photo/865608) - Licence: CC0licence Public Domain

[Unearthing of the Ark](https://en.wikipedia.org/wiki/Levantine_archaeology#/media/File:Jerycho8.jpg) - Licence: Public Domain

### Text and Information

All text and information about all artifacts, historical figures and historical events was taken from [wikipedia](https://www.wikipedia.org/) and shared under licences [Creative Commons Attribution-ShareAlike 3.0 Unported License](https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License) and the [GNU Free Documentation License](https://en.wikipedia.org/wiki/Wikipedia:Text_of_the_GNU_Free_Documentation_License)


