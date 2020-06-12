# tourney
Family basketball tournament scoring system.

## Example
`python example.py` show how to take a simple text format of games:
```
Steve Dave Jim over Brian Gene Shannon
  Shannon Sam Seth over Steve Brian Jim
Dave Gene Seth over Brian Jennn
```

And turn it into a dataframe showing each game and the resulting scores:

```
         Brian         Dave         Gene        Jennn          Jim          Sam         Seth      Shannon        Steve                              Game Summaries
0  1484.000000  1516.000000  1484.000000          NaN  1516.000000          NaN          NaN  1484.000000  1516.000000  Steve, Dave, Jim over Brian, Gene, Shannon
1  1466.530498  1516.000000  1484.000000          NaN  1498.530498  1517.469502  1517.469502  1501.469502  1498.530498   Shannon, Sam, Seth over Steve, Brian, Jim
2  1466.526255  1516.002829  1484.002829  1499.995756  1498.530498  1517.469502  1517.472331  1501.469502  1498.530498          Dave, Gene, Seth over Brian, Jennn
```
