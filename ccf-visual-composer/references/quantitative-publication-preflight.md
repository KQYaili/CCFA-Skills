# Choosing a quantitative comparison

Use the comparison unit, metric and budget defined by the experiment. The [figure design library](figure-design-library.md) lists the corresponding chart implementations. These choices matter when different encodings of the same table would support different interpretations.

| Reader's question | What to plot and check |
| --- | --- |
| How did each task or subject change? | Match observations by ID. A dumbbell shows both levels, and a signed difference shows the change directly. State the subtraction order and units. Report how incomplete pairs were handled. With only aggregate scores, plot those scores and leave individual changes unknown. |
| How certain is a difference or ranking? | Use a supplied estimate of the contrast and its interval when available. Name the interval type, its level where applicable, and the unit used for sampling or resampling. Marginal intervals for two methods cannot by themselves establish the uncertainty of their paired difference. If the source supplies only point estimates, label them accordingly. |
| How does abstention affect performance? | At each threshold, show coverage relative to all eligible cases and risk as the specified loss over the accepted cases. Risk is undefined when no case is accepted. Calibration answers a separate question. For a reliability plot, show how observed outcomes relate to predicted probabilities and give bin counts where available. |
| Can these results be pooled or compared across settings? | Label the split, budget and weighting rule. For example, the mean of task-level rates gives each task equal weight, while pooling event counts weights tasks by their denominators. Use the aggregation the claim specifies. |

For a publication export, compare the displayed values with their source and inspect the figure at its destination width. Follow the [existing export checks](figure-post-render-qa.md). The collision and text-size tools read the final PDF. For comparable panels, the alignment tool reads the measured layout manifest from the same final rendering.
