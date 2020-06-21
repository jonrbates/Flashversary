A web app that simulates flashcards.
It adaptively learns and draws the most challenging cards
using reinforcement learning.

Demo: www.flashversary.com

Dev locally
flask run

Test locally
docker build -t flashversary .
docker run -i -a stdout -a stderr \
     -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
     -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
     -p 8080:5000 \
     --cpus="1" -m 1g \
     flashversary:latest

Deploy to elastic beanstalk after committing branch
[first time] eb init -p docker flashversary
[first time] eb create flashversary-dev -s
eb deploy


Branches
master - arithmetic.  t2.micro is sufficient


Appendix.
See notes/notes.txt for thorough analyses and workflow comments.


Credits.

https://github.com/aws-samples/eb-py-flask-signup/tree/docker
Used this for theme and help with css, js, bootstrap
