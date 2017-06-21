
import praw
import time
import os.path

APP_IDEA1 = "an app where"
APP_IDEA2 = "an app that"
commentsRepliedTo = []

def authenticate():
	print("Authenticating...")
	reddit = praw.Reddit('appideabot', user_agent = "App Idea Bot")
	print("Authenticated as {}".format(reddit.user.me()))

	return reddit


def main():
	reddit = authenticate()
	commentsRepliedTo = getSavedComments()
	runBot(reddit)


def runBot(reddit):
	print("Obtaining 25 comments...")
	for comment in reddit.subreddit('test').comments(limit=25):
		if APP_IDEA1 in comment.body or APP_IDEA2 in comment.body and comment.id not in commentsRepliedTo and comment.author != reddit.user.me():
			print("Found an app idea from " + comment.id)
			saveIdea(comment.body)
			print("Jotted down that idea for possible later production")
			commentsRepliedTo.append(comment.id)
			print("Adding comment ID to list of comments replied to")
			commentIds = open("replies.txt", "a+")
			commentIds.write(str(comment.id) + "\n")
			commentIds.close()

	print("Sleeping for one minute...")
	time.sleep(60)


def saveIdea(comment):
	if not os.path.isfile("appIdeas.txt"):
		ideas = open("appIdeas.txt", "a+")
		ideas.write(str(comment) + "\n\n")
		ideas.close()
	else:
		ideas = open("appIdeas.txt", "a")
		ideas.write(str(comment) + "\n\n")
		ideas.close()


def getSavedComments():
	if not os.path.isfile("replies.txt"):
		commentsRepliedTo = []
		print("This list was created")
	else:
		commentIds = open("replies.txt", "r")
		commentsRepliedTo = [line.strip() for line in commentIds]

	print(commentsRepliedTo)
	return commentsRepliedTo


main()
