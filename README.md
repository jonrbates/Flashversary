A web app that simulates flashcards. It adaptively learns and draws the most challenging cards using reinforcement learning.  Currently, it's set up to demo arithmetic, but can be easily modified for any subject.

**Demo: www.flashversary.com**

Note: To see Q-value updates, click the *Toggle Table* button in the demo.

### Run instructions

*Run locally*
```
flask run
```

*Test locally*
```
docker build -t flashversary .
docker run -i -a stdout -a stderr \
     -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
     -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
     -p 8080:5000 \
     --cpus="1" -m 1g \
     flashversary:latest
```

*Deploy*\
First, commit the branch.

For a first deployment, run these first
```
eb init -p docker flashversary
eb create flashversary-dev -s
```
Then
```
eb deploy
```

### Credits

Source for static theme and fonts:
https://github.com/aws-samples/eb-py-flask-signup

Source for gif: 
https://giphy.com/gifs/monty-cool-cat-happiness-jbKf1K7MhK5DErbeXY
