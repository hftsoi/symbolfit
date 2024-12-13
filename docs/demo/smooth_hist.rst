Histogram smoothing
-------------------

When a histogram with limited statistics needs to be smoothened, we can perform fits to get the smooth functions first, and then convert back to the original binned format. This can be useful for HEP analyses where some signal or background histograms are often statistically limited in the final signal regions due to a series of tight selection cuts applied, and often some other complicated methods are required to convert them into smooth version. This can be handled by SymbolFit as we added an option dedicated to this use case.

.. note::

   stay tuned!
