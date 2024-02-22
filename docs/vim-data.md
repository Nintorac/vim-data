---
title: VIM Data
---

> Note quick afternoon hack, so far might not pursue anytime soon.

The overall idea of this repository is to build a large, high quality dataset of vim edits, for those uninitiated, vim is a keyboard driven text-editor, it uses hot-keys to provide speedy navigation around text documents without needing a mouse. The motivation came after reading [Repeat After Me: Transformers are Better than State Space Models at Copying](https://arxiv.org/abs/2402.01032) where they show that SSMs can't copy, which is a shame because it is quite important. I've also recently started learning vim (notice me Pappa Primeagen), and think the abstractions that it implements present a unique and powerful solution to the problem. 

I am not sure how it would be achieved, but if the model could have multiple "streams of conscious" so to speak, where each stream is a vim buffer, they can be added and removed dynamically with some kind of controller issuing vim commands to build a response to user query iteratively by default. Lofty ideas...for now the plan would just be to build a high quality dataset to teach some network the basics.
