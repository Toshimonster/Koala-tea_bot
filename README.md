# Koala-tea Bot
##### Developed By Joshua, Steven And William.


`python index.py`

We were given a task of creating a quality slack bot, of organising 'Tea rounds' in the office, with added 
functionality to 'name and shame' people in the office.
	'seems simple, right?'
It may have seemed simple to start with, as it does with most projects, so we used 'scrum' to show our ideas.

'We needed to create a bot.'
'So, we need to be able to connect to the slack api.'
'Yeah, but also we need to be able to read when the user puts in "tearound"'
'What about displaying all the teas given during the tearound'
'I think grouping them would be a great idea, in order to increase useability'

This step has to be considered the greatest of them all. Anyone could create a bot, but it has to meet the demands.
Without knowing how to meet the demands, how on earth are you supposed to create it?!

So, we started developing.
Josh, being Josh, was the first to jump on the bandwagon of technicality - He started developing the framework to 
connect to the slack API straight away!
However, the keen Will was not intimidated... - we needed a database of some kind. He started developing the
framework to communicate with the database.
Steve, well he thought outside the box. 'If we need to add commands to the bot, why dont i create a command framework?'
He started doing this, to make implimenting simple features an ease.

After the first day of five, we were able to get the bot to become alive.
"!ping"
"..."
"..."
"Pong!"
You can never understand the happiness from such a little response, until youve tried it 15 times.

In the second day, we set out to get the tea functionality to work.

'We need a tealist, filled with different types of teas'
'But the teas need codenames, such as wt, to make it easy to type'
'What about a custom tea, so if their tea is not on the list?'

We started to work.
We needed some global flags to determine if a tearound is in place. We needed to be able to wait a length of time.
In essence, we needed alot of closely linked parts. We thought that this could really only be done on one workstation, 
due to how close together. Thus, we all gathered by Josh's computer, and started to code. However, before we knew it,
we ran into a problem. A problem which goes against the way python was built.
Syncronous problems.

If somthing is syncronous, then it can only do one thing at a time.
Work out 5+5 -> then send result to website -> then wait for response.
However, we needed stuff to be done while it was waiting for a response.
We needed it to be asyncrounous.

After searching, googling, and even binging, we came up with...

nothing.
.-.

We gave up hope for the day.
Day 2 has ended on a darker side.

However, there was one person who did not give up hope.
'Anything is possible with code' - he knew. Absolutly anything.
So, he looked into how asyncronousity works.
'Threading' - that was the answer.
Josh rushed to test this straight away, even though we had 3 days to go.
Syntax error after Exceptions, and finally, the bot was able to say 'Teatime is 3/4 done!' and end at the right time.
Yes that is it.
Shut up, it was an achivement.

During this however, it was evident that Steve and Will was having fun.
Josh looked at the slack channel and saw.... a bunch of cats and memes.
Cute ones at that, but they seemed to have added !gif, !img, and !cat.
... and apparently 'secret commands', known as 'sekrit commands' from them, but who knows what they are, but them.
This is why coding can be great fun while giving you an education in memeology.

Day 3 Went by fast, I guess we need to limit the caffeene!

Today, we tested the code with those at redriver...
...to be spammed with suggestions, followed by laughs heard around the office!
General debugging went through and new tea-types were added to the recently made list.
Commands were polished and memes were shown in the #sekrit_dokument chat as we attempted to polish the base commands.
Also, More secret commands were added.

Day 4 Began normally, but as always, its never as simple as that.

The day was a fairly simple one - stress-test the bot(get rate-limited in the process), fix bugs and have fun.
Also add in a new tea-time version by the suggestion of our employer.
One major bug that day involved us having to spend an hour looking for a fault...
...only for will to find out that josh simply put in the wrong brackets.
Oh how the simplest of things can break codes so easily. 
Day 4 was as normal as it was going to get.
...Also...
*Hosting!*
_BAM!_
SSH shonanagains...
_BING!_
Ubuntu is a pain with services...
_BOOM!_
`rc.local` ftw.
_~Cheers Paul_

Day 5, The final day.

The last hours we had to polish everything we've done.
The last few hours to take in final requests.
With these last few hours, We, as a group, decided to write this log.
Polish everything, multitasking, if you will.
The bot was now able to accept a multitude of commands and reply.
It could do peroni-time's, tea-time's, show you random cat pictures.
It could even show you a gif of a drifting tank, should you put in the right command.
It was done. Ready for public use..
Our hard work produced a bot worthy of it's name.
and that concludes how the Koala-teabot was made.


