# aws_automations
This is a repository to keep simple automation scripts for AWS

The intention of this repository is to mantain a automation script that I used to solve a use case that I need to automate.

For now you can see 2 scrips, one for stop all instances  doesn't have the specific tag (in this example the tag and value are autotag:no) in the AWS region that the Lambdas was created, the second do the same thing but in multiple regions (you can define with ones you want to use).

To automate it, you can create a Python 3.8 Lambda function and you can a trigger (on the Lambda) with the "EventBridge (CloudWatch Events)" to run in the schedule that you define. If you want to execute it every day at 11PM (GMT-0) you can use Schedule expression: cron(0 23 * * ? *)

