FAQ's
---------


**What is gamba?**

gamba is a transaction analysis library written in Python.
It contains methods for replicating and visualising existing work in the field of player behaviour tracking - a branch of gambling studies focussed on understanding player behaviour for consumer protection.


**How does gamba work?**

Like other Python libraries, gamba is divided into modules, where each module helps answer different questions in the analytic process. For example, the data module contains methods for cleaning and loading transaction data sets. Methods from different modules can be combined to fully recreate analytic processes for a number of academic studies.
They can also be combined in different ways, creating new (novel) analytic processes.


**Who created gamba, and why?**

Oliver J. Scholten started developing gamba in late 2019.
It was developed to make replicating existing research easier, and to help increase the rate of scientific progression in player behaviour tracking.
By open-sourcing the tools needed to replicate existing work, they can be extended and improved much faster than by a single lab/team working in isolation.

**How can I get started?**

To get started using gamba, looking through some of the :any:`research/index` is a great first step. From there, try replacing some of the methods used with others in the library, or load in a new data set and run the same analysis. If you get stuck anywhere or need help, feel free to reach out through `Twitter <https://www.twitter.com/gamba_dev>`_ or by `Email <mailto:oliver@gamba.dev>`_.

**What's the benefit of using gamba?**

By using gamba you have access to methods which can provably replicate existing work. This has a few big benefits - you won't have to re-implement them yourself, you know they're true to the orginal descriptions because they replicate the work, and you can write code which sits on-top of the library's methods, so if anyone wants to replicate your work they'll find it easier (if you also open-source your code). In short, you can use code knowing that it works, without having to test it yourself (but you still can if you want)!

**Why this set of replications?**

The four papers that gamba can currently be used to replicate were the first in a series of papers to use actual internet gambling data to understand player behaviours. By starting at the beginning, we hope to create a foundation on which more recent (and advanced) analytical methods can be replicated, as many use the behavioural measures calculated in this early series.

**Which studies are being replicated next?**
We're currently working to add methods from :any:`these four studies <research/replications/index>` to the gamba library. 
Unlike the first four, these were selected based on their spread across the last few years, and the mix of methods they use. 
Because gamba is open source, if you'd like to add a replication or contribute your code, please see the :any:`development` page!

**Who sponsors gamba's development?**

Nobody.


**Is gamba impartial?**

Yes. All of the code is publicly available, making hiding biases or misrepresenting findings when using gamba very difficult.
This does not mean the data used can't be selectively analysed, but it does mean that the analyses themselves are completely transparent.


**Who can use gamba?**

Anyone, although it's specifically designed for academic research.


**Should I use gamba?**

Yes! If you're studying player behaviours and want to write replicable papers which can tangibly progress our analytical capablities, then use gamba!
Find out more about contributing to gamba on the :any:`development` page.


**How do ethics apply to gamba?**

Ethical concerns are at the heart of gamba's development.
When creating a replication using gamba, ethical approval is always sought from a local institutional review board before any code or examples are published.
Here, that means gaining ethical approval from the Physical Sciences Review Council through the Department of Computer Science at the University of York.
Ethical documentation from this review process is available for each of the example studies on request.





