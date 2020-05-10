Overview
=======================

Aim
----
gamba aims to provide transparent, verifiably accurate implementations of existing research in the field of player behaviour tracking. 
This in turn promotes the development of more effective consumer protection measures, and lets us understand new forms of gambling faster than ever before.

How it works
-------------------
Gambling transaction data typically comes in different structures, from indivdiual poker hands to daily aggregate sports betting. 
The number and type of analytical methods which can be applied to this type of data are equally variable, from simple descriptive statistics to unsupervised machine learning techniques. 
To create a library capable of taking multiple data sources and performing multiple analyses, gamba uses a middle-step between them.

.. raw:: html

    <div class="overview_top">

.. figure:: images/top_level_options.*

.. raw:: html

    </div>

To make this possible, analyses using gamba revolve around the idea of a **measures table**, that is, a dataframe, or table, in a particular format. 
This format has an identifier column (player_id), a collection of behavioural measures columns for each of those players, and (optionally) one or more labelling columns describing each player's membership to a given category or cluster;

.. figure:: images/measures_table.*

This design means that all studies using gamba generally follow a three step process of choosing data, computing behavioural measures, and then applying some analytical technique to those measures. These steps can be repeated using the output of a previous iteration, for example; you may find a particular cohort of players to be of interest following an initial exploration, then take only that cohort and do some further analysis.

.. raw:: html

    <div class="overview_top">

.. figure:: images/simple_workflow.*

.. raw:: html

    </div>

Methods in gamba therefore focus either on getting data into a measures table, or using this format as a foundation for analysis. 
This is reflected in the design of each of the modules in the library. Each module contains methods for answering a specific type of question;

- Which data shall I use in my study? (:any:`gamba.data`)
- Which behavioural measures shall I calculate? (:any:`gamba.measures`)
- Which groups of players are of interest for my study? (:any:`gamba.labels`)
- How would I like to test my hypotheses? (:any:`gamba.tests`)
- How do my data cluster? (:any:`gamba.clustering`)
- How could I plot my findings? (:any:`gamba.plots`)

Splitting the library into modules like this means bits can be swapped out as required, and new (novel) techniques can be discovered more easily than ever before.
It also means that as more studies are reproduced using gamba, the opportunities for exploring different combinations increases multiplicatively!


Why use gamba?
---------------
Player behaviour tracking research as an academic discipline is growing fast. 
As more operators provide data to researchers, new analytical methods are being developed and published by researchers from psychology, computer science, economics, and more.

Until now, no open-source library exists which meets the needs of this growing field - to replicate studies. 
This means researchers need to implement other's methods themselves, which, on top of being a labour intensive task, increases the risk of bugs being introduced, and their own work not being replicable.

gamba aims to provide a collection of methods for reproducing existing work, therefore raising the baseline of the capabilities of researchers in the field - with the ultimate effect of advancing the rate of scientific progress. 
Although gamba can never be a unified framework for reproducing all work in the field, it can provide new and existing researchers with the opportunity to explore analytical code themselves. 
New discoveries, approaches, and insights are inevitable taking this approach. 
By using gamba, and sharing your extensions and experience, you will be helping progress our field in a tangible and impactful way, which will help us all contribute to creating more effective consumer protection measures, and understanding new forms of gambling.


On top of this, the open-source nature of gamba in the context of player behaviour tracking research has several important benefits;

- **reproducibility opposes bias** - because gamba is open source, and because it can replicate studies, researchers who use it inherently promote analytical transparency, decreasing the possibility of hidden bias from funding or stakeholders.
- **transparency promotes learning** - because gamba is open source, all researchers have a lower barrier to entry than ever before to making new discoveries in the field. This means opening the doors for more researchers, more analysts, and better science.
- **methods are available instantly** - by open sourcing implementations of existing methods, they can be quickly applied to existing data, decreasing the time-to-impact and time-to-replication of academic research.
- **methods can be scrutinised** - by publishing analytical code, it can be scrutinised by experienced researchers and programmers who can then improve it. This means more efficient, more accurate code than can be achieved alone, improving the quality of everyone's analytical capabilities.


If you'd like to see how powerful gamba's modular design can be, continue to the :doc:`installation page <installation>`, :doc:`user guide <user_guide/index>`, or on to the :doc:`faqs` for more information.

