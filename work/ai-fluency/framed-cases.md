# Framed Cases — John Andrei Martinez

**Voice card:** direct, plain, honest, still learning, checks my work.

One audience: a hiring manager looking at junior AI/ML people. One thing I want them to do: email me at martinezjandrei8425@gmail.com.

---

## The interview I did (FlyRank project)

I had my AI ask me questions one at a time so I could get the story out before writing anything down. This is the rough version.

**What was the problem?** A page ranks on Google, gets visitors, then slowly loses them. The annoying part is nobody notices until the visitors are already gone. And a company can have thousands of pages, so you can't just go check them all yourself. So it comes down to: which page do you fix first?

**What did you build?** A simple rule first, something like "old page that still gets views, flag it." Then a model that scores every page and sorts them, so the ones most likely to be dying end up at the top.

**What was the hard part?** Testing it honestly. If you test the model on the same pages it already studied, of course it looks smart. So I tested it on companies it had never seen. That's the fair test.

**Anything surprise you?** Yeah. My model looked great on the easy test, and on the fair one it could not be told apart from my simple rule. I left that in. Felt more useful to be honest about it than to hide it.

---

## FlyRank — which page to fix first (my internship project)

A page gets found on Google and then quietly loses its visitors over time. Most teams catch it too late. There are way too many pages to go through by hand, so you have to decide which ones to fix first.

I started with a simple rule so I'd have something to beat, then built a model that scores each page and puts the riskiest ones at the top of the list. The part I spent the most time on was how to test it fairly — I tested on companies the model hadn't seen instead of the ones it learned from. My own model looked clearly better on the easy test, then on the fair test the gap shrank to nothing I could defend, and I kept that result.

On the fair test the sorted list got about three times more of the right pages up top than the simple rule did. Honestly the number matters less to me than being able to explain why it works, and when a plain rule is actually the better choice.

## ACRA — making signs readable for color-blind people (my thesis)

A lot of public signs use color to mean something, but roughly 1 in 12 men can't tell those colors apart. You can't fix a whole city's signs one at a time.

So I taught a model to find the spots on a sign where color carries the meaning, then built the part that shifts those colors just enough for a color-blind person to read them, without ruining how the sign looks. I labeled around 33,000 examples by hand — tedious, but the model is only as good as the examples you feed it. Then I put it online so anyone can upload a photo and get a fixed version, and made it delete their photo after a day.

It scored 0.740 on my own test set (out of 1, higher is better), and the full thing runs start to finish: photo in, readable sign out.

## Aegix AI — checking job contracts against the law

When someone gets a job contract, they usually can't tell which parts are unfair or illegal, and a lawyer costs more than the job is worth.

I built a tool that reads a contract clause by clause and checks each one against Philippine labor law. For every clause it says fine, not fine, unclear, or missing, points to the exact law, and explains why in plain words. I broke the checking into small steps so you can see how it decided, ran them at the same time to speed it up, and showed results as they came in. I also put together a small set of contracts with known answers so I could actually measure whether it was right, instead of guessing.

On 18 contracts I'd checked myself it agreed with the right answer 84.5% of the time, caught every problem clause, and cited the correct law 94.8% of the time.

---

## About me

I'm John Andrei, a Computer Science student in Bulacan, Philippines. I build machine-learning tools on real, messy data, and I try to show the testing behind my numbers instead of just claiming them. I like building the whole thing — the data part, the model, and the finished tool you can actually click.

## Contact

Hiring a junior AI/ML or data person and want someone who'll tell you when a number doesn't hold up? Email me at **martinezjandrei8425@gmail.com**. Code's at github.com/Zeref538.

---

## Before / after

**Generic AI line:**
> Results-driven machine learning engineer passionate about leveraging cutting-edge AI to deliver impactful, scalable solutions that drive business value.

**Mine:**
> I train models on messy real data and keep the number that survives an honest test — even when it's worse than I hoped for.
