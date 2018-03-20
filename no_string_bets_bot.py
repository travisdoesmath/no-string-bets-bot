# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 03:12:22 2018

@author: Travis
"""

import collections, praw, re, warnings

r = praw.Reddit(user_agent='NoStringBetsBot v0.1',
                  client_id=os.getenv("CLIENT_ID"),
                  client_secret=os.getenv("CLIENT_SECRET"),
                  username='no_string_bets',
                  password=os.getenv("PASSWORD"))
                     
#This is simple collection of functions to prevent reddit bots from:
#1. replying twice to same summon
#2. prevent chain of summons
#3. have limit on number of replies per submission

#Note: See TODO and make according changes
#Note: You can use reply function like this: post_reply(comment-content,praw-comment-object)
#Note: is_summon_chain returns True if grandparent comment is bot's own
#Note: comment_limit_reached returns True if current will be 5th reply in same thread, resets on process restart
#Note: don't forget to decalre `submissioncount = collections.Counter()` before starting your main loop
#Note: Here, r = praw.Reddit('unique client identifier')

def is_summon_chain(post):
  if not post.is_root:
    parent_comment = post.parent()
    if parent_comment.author != None and str(parent_comment.author.name) == 'no_string_bets': #TODO put your bot username here
      return True
    else:
      return False
  else:
    return False
  
def comment_limit_reached(post):
  global submissioncount
  count_of_this = int(float(submissioncount[str(post.submission.id)]))
  if count_of_this > 4: #TODO change the number accordingly. float("inf") for infinite (Caution!)
    return True
  else:
    return False
  
def is_already_done(post):
  done = False
  numofr = 0
  try:
    repliesarray = post.replies
    numofr = len(list(repliesarray))
  except:
    pass
  if numofr != 0:
    for repl in post.replies:
      if repl.author != None and repl.author.name == 'no_string_bets': #TODO put your bot username here
        done = True
        continue
  if done:
    return True
  else:
    return False

def is_serious_post(post):
    if '[serious]' in post.submission.title.lower(): return True
    else: 
    return False

def post_reply(reply,post):
  global submissioncount
  try:
    a = post.reply(reply)
    submissioncount[str(post.submission.id)]+=1
    return True
  except Exception as e:
    warnings.warn("REPLY FAILED: %s @ %s"%(e,post.subreddit))
    if str(e) == '403 Client Error: Forbidden':
      print(f'/r/{post.subreddit} has banned me.')
    return False

submissioncount = collections.Counter()

subreddit = r.subreddit('travisdoesmath')
for comment in subreddit.stream.comments():
    if re.search("(I see your)( *[a-zA-Z]* *){0,10}(and raise you)", comment.body) \
        and not(is_summon_chain(comment)) \
        and not(comment_limit_reached(comment)) \
        and not(is_already_done(comment)) \
        and not(is_serious_post(comment)): post_reply("no string bets, please!\n\n---\n^^I'm ^^a ^^bot, ^^learn ^^more ^^about ^^string ^^bets ^^[here](https://en.wiktionary.org/wiki/string_bet)", comment)
