'''
CMS search for trijet resonances at sqrt(s) = 13 TeV
    https://arxiv.org/abs/2310.14023
    https://doi.org/10.1103/PhysRevLett.133.011801

Invariant mass spectra of trijet events (Figure 1), public data taken from HEPDATA
    https://www.hepdata.net/record/ins2713513
'''


x=[
#1531. , 1594. , 1659. , 1726. ,
1794. , 1863.5, 1935.5, 2009.5,
       2085.5, 2163.5, 2243.5, 2325.5, 2409.5, 2495.5, 2583.5, 2673.5,
       2766. , 2861. , 2958. ,
       #3057.5, 3159.5, 3264. , 3371. , 3480.5,
       #3592.5, 3707. , 3824.5, 3945. , 4068. , 4193.5, 4322. , 4453.5,
       #4588. ,
       #4726. ,
       #4867.5,
       5012. , 5160. , 5311.5, 5466. , 5624. ,
       5786. , 5951.5, 6120.5, 6293.5, 6470.5, 6651.5, 6836.5, 7025.5,
       7219. ,
       #7417. , 7619. , 7825.5, 8037. , 8253. , 8473.5, 8699. ,
       #8929.5, 9165. , 9405.5, 9651.5
       ]

y=[
#151178.0,
#121096.0,
#97684.0,
#77400.0,
231784.0,
188875.0,
149875.0,
119619.0,
94933.0,
75791.0,
60420.0,
47741.0,
37905.0,
29733.0,
23696.0,
18854.0,
14937.0,
11535.0,
9181.0,
#7277.0,
#5669.0,
#4493.0,
#3535.0,
#2863.0,
#2146.0,
#1601.0,
#1310.0,
#1066.0,
#780.0,
#585.0,
#465.0,
#335.0,
#233.0,
#186.0,
#152.0,
93.0,
91.0,
66.0,
50.0,
25.0,
29.0,
16.0,
13.0,
12.0,
4.0,
2.0,
2.0,
2.0,
1.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0
]

y_up=[
#389.817,
#348.989,
#313.545,
#279.21,
482.44,
435.598,
388.138,
346.861,
309.113,
276.303,
246.806,
219.499,
195.694,
173.435,
154.937,
138.312,
123.22,
108.404,
96.821,
#86.3092,
#76.2972,
#68.0348,
#60.4615,
#54.5132,
#47.3321,
#41.0208,
#37.2031,
#33.6599,
#28.9404,
#25.2006,
#22.5793,
#19.3212,
#16.2862,
#14.6626,
#13.3559,
10.6782,
10.5744,
9.16509,
8.11822,
6.06659,
6.44702,
5.08307,
4.69757,
4.55982,
3.16275,
2.63786,
2.63786,
2.63786,
2.29953,
#1.84102,
#1.84102,
#1.84102,
#1.84102,
#1.84102,
#1.84102,
#1.84102,
#1.84102,
#1.84102,
#1.84102,
#1.84102,
#1.84102
]

y_down=[
#388.816,
#347.988,
#312.544,
#278.208,
481.439,
434.597,
387.136,
345.859,
308.111,
275.301,
245.804,
218.496,
194.691,
172.432,
153.934,
137.309,
122.216,
107.4,
95.8158,
#85.3034,
#75.2905,
#67.0274,
#59.4531,
#53.5039,
#46.3213,
#40.0083,
#36.1893,
#32.6445,
#27.9225,
#24.1799,
#21.5561,
#18.2939,
#15.2534,
#13.6259,
#12.3153,
9.62628,
9.52183,
8.1034,
7.04734,
4.96633,
5.35393,
3.9578,
3.55866,
3.41527,
1.91434,
1.29181,
1.29181,
1.29181,
0.827246,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0,
#0.0
]
 
bin_widths_1d=[
#62.,  64.,  66.,  68.,
68.,  71.,  73.,  75.,  77.,  79.,  81.,
        83.,  85.,  87.,  89.,  91.,  94.,  96.,  98.,
        #101., 103., #106.,
       #108., 111., 113., 116., 119., 122., 124., 127., 130., 133., 136.,
       #140.,
       #143.,
       146., 150., 153., 156., 160., 164., 167., 171., 175.,
       179., 183., 187., 191., 196.,
       #200., 204., 209., 214., 218., 223.,
       #228., 233., 238., 243., 249.
       ]