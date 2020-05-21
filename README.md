# Flask + AWS service toy project

*Disclaimer:* This project was not built from scratch, it started from [GCPtutorial](https://github.com/GoogleCloudPlatform/getting-started-python) It was intended to be deployed in Google Cloud Platform, which I did it as a school project about an year ago. (KAIST EE488G) 

But I wanted to deploy this project in AWS environment using Elastic Beanstalk, and use the relational database from AWS. Also, I made some upgrades like recommendation or seeding some initial data set. 

## TODO

- Find a better thumbnail? (numerous cat pics are driving me crazy)
    - google image scraping?
    - where to store thumbnail images? S3?
- Book recommendation based on description?
    - Should study [text_similarity](https://medium.com/@adriensieg/text-similarities-da019229c894)
    - Since there is no plan for implementing multiple users, user-user collaborative filtering strategy is not a good fit.

## Seeding data set

Used [this](https://www.kaggle.com/jrobischon/wikipedia-movie-plots). Yeah I know. This is not a book dataset, but it's about movie. But this one had the most extensive description (which would help my text similarity embedding...) and the most reasonable file size.

I added initialization routing in crud.py. And wrangled the description file using regular expression.

## Trouble shooting

### Elastic Beanstalk doesn't work as intended

There were two causes for this issue.

#### Elastic Beanstalk searches for "application" not "app!"

This was particularly bugging for me, since the official document of flask defines and calls "app" not "application". So I changed all app Flask object to object named application. Additionally, I had to change the filename "main.py" to "application.py". (thx to [officialdocument](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html))

#### Redundant requirements

```terminal
\$ eb create
```

kept failing with exit status 1

**Solution** Removed unnecessary components from requirements.txt (especially pandas...) (thx to [this_forum](https://forums.aws.amazon.com/thread.jspa?messageID=896593))

### ALB health check failure

Health check kept giving me the result: Severe : Target.ResponseCodeMismatch

After digging into [resolution](https://aws.amazon.com/premiumsupport/knowledge-center/elb-fix-failing-health-checks-alb/), I found out that the solution was in the logs. Server response showed that my application was sending HTTP 302 response code when the user enters into the site. 

So I just added 302 to the success codes in configuration of *target groups*, since it didn't seem problematic to me...

![what-a-soothing-figure](https://i.imgur.com/sQoGBXS.png)

## References

- [Flask+AWS](https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80)
- []
