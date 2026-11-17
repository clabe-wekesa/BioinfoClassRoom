#!/usr/bin/env python
# coding: utf-8

# <style>
# .jp-CodeCell, .code_cell {border-left: 5px solid #2e7d32 !important;}
# .jp-InputArea, div.input_area {background: #f1f8e9 !important;}
# .jp-OutputArea, div.output_area {background: #fbfff8 !important;}
# .note {background:#eef6ff; border-left:5px solid #1976d2; padding:10px 14px;}
# .warning {background:#fff8e1; border-left:5px solid #f9a825; padding:10px 14px;}
# .activity {background:#f3e5f5; border-left:5px solid #7b1fa2; padding:10px 14px;}
# </style>
# 
# # SBI 811: Computer Programming in Bioinformatics
# ## Lecture 8 — Applications of Python in Bioinformatics I
# 
# ### From biological questions to algorithms
# 
# **Duration:** approximately 3 hours  
# **Level:** introductory  
# **Prerequisite:** variables, strings, lists, dictionaries, loops, conditions, functions and basic file handling
# 
# In earlier lectures, individual Python tools were studied separately. This lecture brings those tools together. The central question is no longer only *“What does this line of Python mean?”* It is now also:
# 
# > **How can a biological or biochemical problem be divided into small steps that a computer can perform?**
# 

# ## Learning outcomes
# 
# By the end of the lecture, a student should be able to:
# 
# 1. translate a scientific question into inputs, processing steps and outputs;
# 2. read several DNA sequences from a FASTA file and calculate simple summaries;
# 3. explain the main idea of dynamic programming in ordinary language;
# 4. fill a small sequence-alignment scoring table by hand;
# 5. implement Hamming distance and edit distance using beginner-level Python;
# 6. explain the Michaelis–Menten equation and identify its variables;
# 7. plot enzyme velocity against substrate concentration;
# 8. construct and interpret a Lineweaver–Burk plot;
# 9. recognise important limitations of a computational result.
# 

# ## Lecture map
# 
# | Approximate time | Topic |
# |---:|---|
# | 0–15 min | From a scientific question to an algorithm |
# | 15–40 min | Application 1: FASTA sequence summaries |
# | 40–50 min | Short break or recap |
# | 50–115 min | Application 2: dynamic programming and sequence alignment |
# | 115–125 min | Short break |
# | 125–165 min | Application 3: enzyme kinetics and plots |
# | 165–180 min | Exercises, interpretation and review |
# 
# The final section may be continued in the next practical if students need more time. Understanding the logic is more important than finishing every optional activity.
# 

# # Part 1 — From a scientific question to an algorithm
# 
# An **algorithm** is a finite sequence of unambiguous steps for solving a problem. A recipe is an everyday example: it identifies the ingredients, the order of operations and the expected product.
# 
# A computational biology problem usually contains three broad parts:
# 
# | Part | Question | Example |
# |---|---|---|
# | Input | What information enters the analysis? | DNA sequences |
# | Processing | What operations are performed? | count G and C bases |
# | Output | What result is produced? | GC percentage |
# 
# Before writing code, describe these parts in plain language. This prevents the program from becoming a collection of commands with no clear scientific purpose.
# 

# ## Example problem
# 
# **Scientific question:** What percentage of a DNA sequence consists of guanine (G) and cytosine (C)?
# 
# One possible algorithm is:
# 
# 1. obtain the DNA sequence;
# 2. convert it to uppercase;
# 3. remove unwanted spaces and line breaks;
# 4. count `G`;
# 5. count `C`;
# 6. add the two counts;
# 7. divide by the sequence length;
# 8. multiply by 100;
# 9. report the percentage.
# 
# This description is **pseudocode**: it expresses the logic without requiring exact Python syntax.
# 

# 
# ### Converting the Algorithm into Python
# 
# The GC content of a DNA sequence is calculated using the following formula:
# 
# $$
# \text{GC content (\%)} = \frac{n_G + n_C}{L} \times 100
# $$
# 
# where:
# 
# - $n_G$ = number of guanine (G) bases
# - $n_C$ = number of cytosine (C) bases
# - $L$ = total length of the DNA sequence
# 
# In Python, we can calculate GC content by counting the G and C bases, dividing their sum by the total sequence length, and multiplying by 100.

# In[ ]:


dna = "ATGCGTAA"
dna = dna.upper().strip()

g_count = dna.count("G")
c_count = dna.count("C")
sequence_length = len(dna)

gc_percent = (g_count + c_count) / sequence_length * 100

print("Sequence:", dna)
print("Length:", sequence_length)
print("GC percentage:", round(gc_percent, 2))


# # Part 3 — Application 2: comparing biological sequences
# 
# Two short algorithms will be studied in this section:
# 
# 1. **Hamming distance**, which counts differences at corresponding positions;
# 2. **edit distance**, which finds the smallest number of edits needed to change one sequence into another.
# 
# Hamming distance is introduced first because it uses familiar ideas: `zip()`, a loop, an `if` statement and a counter. Edit distance then demonstrates why a table and dynamic programming are useful when insertions and deletions are possible.
# 

# ## 3.1 What does “distance” mean for sequences?
# 
# In ordinary language, distance describes how far apart two objects are. For sequences, a distance is a number describing how different they are under a particular rule.
# 
# - A distance of `0` means that the two sequences are identical under that rule.
# - A larger distance means that more differences were detected.
# 
# The number is meaningful only when the rule used to calculate it is stated. Hamming distance and edit distance do not use exactly the same rule.
# 

# ## 3.2 Hamming distance
# 
# **Hamming distance** is the number of positions at which two equal-length sequences contain different characters.
# 
# Consider:
# 
# ```text
# Sequence 1: A T G C C G T A
# Sequence 2: A T G T C G A A
#                   ↑     ↑
# Position:   1 2 3 4 5 6 7 8
# ```
# 
# The bases differ at positions 4 and 7. Therefore, the Hamming distance is 2.
# 
# <div class="warning"><b>Restriction:</b> ordinary Hamming distance requires sequences of equal length. It can recognise substitutions, but it does not directly handle insertions or deletions.</div>
# 

# ### Hamming distance by hand
# 
# Use these steps:
# 
# 1. confirm that the sequences have equal length;
# 2. place one sequence above the other;
# 3. compare the first pair of characters;
# 4. add 1 when the characters differ;
# 5. repeat for every position;
# 6. report the final count.
# 
# ### Pseudocode
# 
# ```text
# IF the sequence lengths are different
#     report that Hamming distance cannot be calculated
# ELSE
#     set distance to zero
#     FOR every position
#         IF the two characters are different
#             add one to distance
#     END FOR
#     report distance
# ```
# 

# In[ ]:


sequence_1 = "ATGCCGTA"
sequence_2 = "ATGTCGAA"

distance = 0

for base_1, base_2 in zip(sequence_1, sequence_2):
    if base_1 != base_2:
        distance = distance + 1

print("Hamming distance:", distance)


# ### Reading the loop carefully
# 
# - `zip(sequence_1, sequence_2)` pairs characters occupying corresponding positions.
# - In each iteration, `base_1` receives a character from the first sequence and `base_2` receives the corresponding character from the second sequence.
# - `!=` means “is not equal to.”
# - The counter increases only when the paired bases are different.
# 
# For example, the first iteration produces `("A", "A")`. A later iteration produces `("C", "T")`, which is counted as a mismatch.
# 
# <div class="warning"><b>Important:</b> <code>zip()</code> stops when the shorter sequence ends. We therefore check that the sequences have equal lengths before using it to calculate Hamming distance.</div>
# 

# ### Make Hamming distance reusable
# 
# A function should check the equal-length requirement instead of silently returning a misleading answer.
# 

# In[2]:


def hamming_distance(sequence_1, sequence_2):
    """Return the number of mismatching positions in equal-length sequences."""
    sequence_1 = sequence_1.upper().strip()
    sequence_2 = sequence_2.upper().strip()

    if len(sequence_1) != len(sequence_2):
        return f"Ensure that sequences have the same length"

    distance = 0

    for base_1, base_2 in zip(sequence_1, sequence_2):
        if base_1 != base_2:
            distance = distance + 1

    return distance


# In[3]:


print(hamming_distance("ATGCCGTA", "ATGTCGAA"))
print(hamming_distance("ACTG", "ACT"))


# The second call returns `None` because the sequence lengths differ. Here, `None` does not mean that the distance is zero. It means that the requested calculation was not valid under the Hamming-distance rule.
# 

# ## 3.3 Why Hamming distance is sometimes insufficient
# 
# Consider:
# 
# ```text
# Sequence 1: ATGCT
# Sequence 2: ATCT
# ```
# 
# The sequences have different lengths, so Hamming distance cannot compare them directly. However, deleting `G` from the first sequence produces the second sequence:
# 
# ```text
# ATGCT  →  ATCT
#   delete G
# ```
# 
# Only one edit is required. This motivates **edit distance**.
# 

# ## 3.4 Edit distance
# 
# **Edit distance**, also called **Levenshtein distance**, is the minimum number of permitted edits needed to transform one sequence into another.
# 
# In the standard version, each operation costs 1:
# 
# | Operation | Meaning | Example |
# |---|---|---|
# | substitution | replace one character | `A` becomes `G` |
# | insertion | add one character | `AT` becomes `ACT` |
# | deletion | remove one character | `ACT` becomes `AT` |
# 
# A matching pair costs 0 because no edit is needed.
# 

# 
# ### The Edit-Distance Rule
# 
# To fill each empty cell in the edit-distance table, we calculate three possible values:
# 
# 1. **Deletion:** Take the value from the cell above and add 1.
# 2. **Insertion:** Take the value from the cell to the left and add 1.
# 3. **Substitution or match:** Take the value from the diagonal cell (top-left). Add 0 if the two characters match, or 1 if they are different.
# 
# The edit distance for the current cell is the **smallest of these three values**.
# 
# Mathematically, this is written as:
# 
# $$
# D(i,j) = \min
# \begin{cases}
# D(i-1,j)+1 & \text{Deletion}\\
# D(i,j-1)+1 & \text{Insertion}\\
# D(i-1,j-1)+c & \text{Substitution or match}
# \end{cases}
# $$
# 
# where:
# 
# - $D(i,j)$ is the value of the current cell.
# - $i$ represents the current row.
# - $j$ represents the current column.
# - $c=0$ if the two characters match.
# - $c=1$ if the two characters are different.
# 
# ### Hand Activity: Calculate Edit Distance
# 
# Complete the following table for the sequences `GAT` and `GC`.
# 
# |       | **–** | **G** | **C** |
# |------:|------:|------:|------:|
# | **–** | 0 | 1 | 2 |
# | **G** | 1 | ? | ? |
# | **A** | 2 | ? | ? |
# | **T** | 3 | ? | ? |
# 
# For each empty cell:
# 
# 1. Calculate the deletion value (top cell + 1).
# 2. Calculate the insertion value (left cell + 1).
# 3. Calculate the diagonal value (top-left cell + 0 or 1).
# 4. Select the smallest value and enter it into the table.
# 
# **Remember:** The value in the bottom-right cell is the minimum number of edits required to transform `GAT` into `GC`.
# 

# # Part 4 — Application 3: enzyme kinetics
# 
# ## 4.1 The biological question
# 
# An enzyme converts substrate into product. In a simple experiment, the initial reaction velocity is measured at several substrate concentrations.
# 
# Typical questions include:
# 
# - Does velocity increase when substrate concentration increases?
# - Does the reaction approach a maximum velocity?
# - What are the approximate values of \(V_{max}\) and \(K_m\)?
# 
# The supplied file `lecture08_enzyme_kinetics.csv` contains substrate concentration and measured initial velocity.
# 

# In[ ]:


kinetics_data = pd.read_csv("lecture08_enzyme_kinetics.csv")
kinetics_data


# ## 4.2 Understand the columns before calculating
# 
# | Column | Meaning | Unit |
# |---|---|---|
# | `substrate_mM` | substrate concentration, \([S]\) | millimolar (mM) |
# | `velocity_umol_per_min` | measured initial velocity, \(v\) | micromoles per minute |
# 
# Units must be retained. A number without its unit can easily be misinterpreted.
# 

# In[ ]:


print(kinetics_data.shape)
print(kinetics_data.dtypes)
print(kinetics_data.isna().sum())


# The checks answer three basic questions:
# 
# 1. How many rows and columns were read?
# 2. Did the numeric columns become numeric data types?
# 3. Are any values missing?
# 
# These checks should occur before plotting or fitting a model.
# 

# ## 4.3 Plot the observed data
# 
# A scatter plot displays each measured pair of substrate concentration and velocity. Connecting points with a line can help the eye follow the pattern, but the line between points is not automatically a fitted biochemical model.
# 

# In[ ]:


import matplotlib.pyplot as plt

substrate = kinetics_data["substrate_mM"]
velocity = kinetics_data["velocity_umol_per_min"]

plt.figure(figsize=(7, 4.5))
plt.scatter(substrate, velocity, color="darkgreen", s=60, label="Observed data")
plt.plot(substrate, velocity, color="lightgreen", alpha=0.7)
plt.xlabel("Substrate concentration [S] (mM)")
plt.ylabel("Initial velocity v (µmol/min)")
plt.title("Observed enzyme-kinetics data")
plt.grid(alpha=0.25)
plt.legend()
plt.show()


# ## 4.4 The Michaelis–Menten equation
# 
# For a simple Michaelis–Menten system,
# 
# \[
# v=\frac{V_{max}[S]}{K_m+[S]}.
# \]
# 
# | Symbol | Meaning |
# |---|---|
# | \(v\) | initial reaction velocity |
# | \([S]\) | substrate concentration |
# | \(V_{max}\) | maximum velocity approached at high substrate concentration |
# | \(K_m\) | substrate concentration at which \(v=V_{max}/2\) |
# 
# The curve rises rapidly at low substrate concentration and then approaches a plateau. It approaches \(V_{max}\), but the mathematical curve does not need to touch it at a finite substrate concentration.
# 

# ## 4.5 Write the equation as a Python function
# 
# The function accepts substrate concentration, \(V_{max}\) and \(K_m\), and returns the predicted velocity.
# 

# In[ ]:


def michaelis_menten(substrate_concentration, vmax, km):
    predicted_velocity = (
        vmax * substrate_concentration
        / (km + substrate_concentration)
    )
    return predicted_velocity


example_velocity = michaelis_menten(2.0, vmax=50.0, km=2.0)
print("Predicted velocity:", example_velocity, "µmol/min")


# In the example, substrate concentration equals \(K_m\). The predicted velocity is therefore half of \(V_{max}\): 25 µmol/min.
# 
# This is a useful reasonableness check. Scientific code should be checked using values whose answers can be predicted.
# 

# 
# ## 4.6 The Lineweaver–Burk Transformation
# 
# The Michaelis–Menten equation describes the relationship between substrate concentration and reaction velocity:
# 
# $$
# v = \frac{V_{\max}[S]}{K_m + [S]}
# $$
# 
# By taking the reciprocal of both sides and rearranging, we obtain the **Lineweaver–Burk equation**:
# 
# $$
# \frac{1}{v} = \frac{K_m}{V_{\max}} \times \frac{1}{[S]} + \frac{1}{V_{\max}}
# $$
# 
# This equation has the same form as the equation of a straight line:
# 
# $$
# y = mx + c
# $$
# 
# where:
# 
# - $y$ is the value plotted on the vertical axis.
# - $x$ is the value plotted on the horizontal axis.
# - $m$ is the slope (gradient) of the line.
# - $c$ is the y-intercept (where the line crosses the vertical axis).
# 
# ### Relationship Between the Two Equations
# 
# | Straight-line quantity | Enzyme-kinetics quantity |
# |---|---|
# | $y$ | $1/v$ |
# | $x$ | $1/[S]$ |
# | Slope ($m$) | $K_m/V_{\max}$ |
# | Y-intercept ($c$) | $1/V_{\max}$ |
# | X-intercept ($-c/m$) | $-1/K_m$ |
# 
# ### Biological Interpretation
# 
# In a Lineweaver–Burk plot:
# 
# 1. The **x-axis** represents the reciprocal of substrate concentration, $1/[S]$.
# 2. The **y-axis** represents the reciprocal of reaction velocity, $1/v$.
# 3. The **slope** of the line is $K_m/V_{\max}$.
# 4. The **y-intercept** is $1/V_{\max}$, so $V_{\max}$ can be calculated by taking its reciprocal.
# 5. The **x-intercept** is $-1/K_m$, which can be used to calculate $K_m$.
# 
# **Important:** The Lineweaver–Burk transformation converts the curved Michaelis–Menten relationship into a straight line, making it easier to visualize the relationship between the kinetic parameters. However, for accurate parameter estimation from experimental data, direct nonlinear fitting of the Michaelis–Menten equation is generally preferred.
# 

# ## 4.7 Calculate reciprocal columns
# 
# Reciprocal means “one divided by the value.” A substrate concentration or velocity of zero would cause division by zero, so the data must be checked first.
# 

# In[ ]:


has_zero_substrate = (kinetics_data["substrate_mM"] == 0).any()
has_zero_velocity = (kinetics_data["velocity_umol_per_min"] == 0).any()

print("Zero substrate value present:", has_zero_substrate)
print("Zero velocity value present:", has_zero_velocity)


# In[ ]:


lineweaver_data = kinetics_data.copy()

lineweaver_data["inverse_substrate"] = (
    1 / lineweaver_data["substrate_mM"]
)
lineweaver_data["inverse_velocity"] = (
    1 / lineweaver_data["velocity_umol_per_min"]
)

lineweaver_data


# The original columns were preserved by creating `lineweaver_data` with `.copy()`. The two new columns are derived values and have reciprocal units.
# 

# ## 4.8 Fit the straight line
# 
# `numpy.polyfit(x, y, 1)` fits a polynomial of degree 1, which is a straight line. It returns the slope and intercept.
# 
# The third argument is `1` because the model is \(mx+c\). A degree of 2 would describe a quadratic curve and would not represent the Lineweaver–Burk equation.
# 

# In[ ]:


import numpy as np

x = lineweaver_data["inverse_substrate"]
y = lineweaver_data["inverse_velocity"]

slope, intercept = np.polyfit(x, y, 1)

print("Slope:", slope)
print("Y-intercept:", intercept)


# ## 4.9 Recover \(V_{max}\) and \(K_m\)
# 
# From the intercept,
# 
# \[
# V_{max}=\frac{1}{\text{intercept}}.
# \]
# 
# From the slope,
# 
# \[
# K_m=\text{slope}\times V_{max}.
# \]
# 

# In[ ]:


estimated_vmax = 1 / intercept
estimated_km = slope * estimated_vmax

print("Estimated Vmax:", round(estimated_vmax, 2), "µmol/min")
print("Estimated Km:", round(estimated_km, 2), "mM")


# ## 4.10 Draw the Lineweaver–Burk plot
# 
# The fitted line is calculated over an ordered range of x-values. Ordering prevents the plotted line from jumping backwards and forwards.
# 

# In[ ]:


x_line = np.linspace(x.min(), x.max(), 100)
y_line = slope * x_line + intercept

plt.figure(figsize=(7, 4.5))
plt.scatter(x, y, color="navy", s=60, label="Reciprocal observations")
plt.plot(x_line, y_line, color="orange", label="Fitted straight line")
plt.xlabel("1 / [S] (1/mM)")
plt.ylabel("1 / v (min/µmol)")
plt.title("Lineweaver–Burk plot")
plt.grid(alpha=0.25)
plt.legend()
plt.show()


# ## 4.11 Plot the estimated Michaelis–Menten curve
# 
# We now use the estimated parameters in the original nonlinear equation. The smooth substrate range begins at zero and extends slightly beyond the largest measurement.
# 

# In[ ]:


smooth_substrate = np.linspace(0, substrate.max() * 1.1, 200)
predicted_velocity = michaelis_menten(
    smooth_substrate,
    vmax=estimated_vmax,
    km=estimated_km,
)

plt.figure(figsize=(7, 4.5))
plt.scatter(substrate, velocity, color="darkgreen", s=60, label="Observed data")
plt.plot(
    smooth_substrate,
    predicted_velocity,
    color="black",
    label="Estimated Michaelis–Menten curve",
)
plt.axhline(
    estimated_vmax,
    color="red",
    linestyle="--",
    label="Estimated Vmax",
)
plt.xlabel("Substrate concentration [S] (mM)")
plt.ylabel("Initial velocity v (µmol/min)")
plt.title("Michaelis–Menten model and observations")
plt.grid(alpha=0.25)
plt.legend()
plt.show()


# ## 4.12 Interpret the result scientifically
# 
# A sound interpretation distinguishes observations from model estimates:
# 
# - The observed velocity increases with substrate concentration.
# - The increases become smaller at high substrate concentrations, suggesting approach to a plateau.
# - The fitted parameters describe this dataset under the assumed Michaelis–Menten model.
# - \(K_m\) has the same concentration unit as the substrate data.
# - \(V_{max}\) has the same velocity unit as the measured reaction rate.
# 
# Avoid writing that the calculation proves the enzyme follows Michaelis–Menten kinetics. Other mechanisms, experimental error or inhibition may also affect the data.
# 

# ## 4.13 An important limitation of Lineweaver–Burk plots
# 
# Taking reciprocals magnifies the influence of small substrate concentrations and small velocities. Experimental error at the lower end can therefore have a disproportionately large effect on the fitted line.
# 
# Historically, Lineweaver–Burk plots were useful for visualisation and hand calculation. Modern analyses commonly estimate \(V_{max}\) and \(K_m\) by fitting the original nonlinear Michaelis–Menten equation directly.
# 
# For this course, the reciprocal plot remains valuable because it connects:
# 
# - algebraic transformation;
# - straight-line fitting;
# - plotting;
# - biological interpretation;
# - critical evaluation of a method.
# 

# # Part 5 — Bringing the applications together
# 
# Although sequence alignment and enzyme kinetics appear different, their computational structure is similar.
# 
# | Stage | Sequence application | Enzyme application |
# |---|---|---|
# | Input | two DNA sequences | concentrations and velocities |
# | Validation | check characters/lengths | check types, missing values and zeros |
# | Model or rules | mismatch counts and edit costs | Michaelis–Menten equation |
# | Computation | fill a dynamic-programming table | transform and fit data |
# | Output | Hamming or edit distance | plots, \(V_{max}\) and \(K_m\) |
# | Interpretation | sequence similarity under chosen scores | kinetic parameters under chosen model |
# | Limitation | scoring system and possible ties | error magnification in reciprocal plot |
# 
# Computational biology is not only about obtaining output. It also requires knowing what assumptions produced that output.
# 

# # Part 6 — Guided exercises
# 
# ## Exercise 1: sequence-quality summary
# 
# Using the `sequences` dictionary:
# 
# 1. calculate the percentage of `N` bases for every sequence;
# 2. add the result to each summary row as `N_percent`;
# 3. classify a sequence as `acceptable` when `N_percent <= 5`, otherwise classify it as `review`;
# 4. print the identifier, percentage and classification.
# 
# ### Pseudocode
# 
# ```text
# FOR each identifier and sequence
#     calculate sequence length
#     count N bases
#     calculate N percentage
#     IF N percentage is at most 5
#         label as acceptable
#     ELSE
#         label as review
#     print the result
# END FOR
# ```
# 

# In[ ]:


# Write Exercise 1 here.


# ## Exercise 2: dynamic-programming table
# 
# Use `edit_distance()` to compare:
# 
# 1. `GAT` with `GCT`;
# 2. `GAT` with `GA`;
# 3. `GAT` with `GAT`.
# 
# Before running the function, predict which pair should have the smallest distance. Explain the result in biological language.
# 

# In[ ]:


# Write Exercise 2 here.


# ## Exercise 3: choose the appropriate distance
# 
# For each pair below, decide whether ordinary Hamming distance can be calculated. Then calculate edit distance for every pair.
# 
# 1. `ACTG` and `ATTG`;
# 2. `ACTG` and `ATG`;
# 3. `ACTG` and `ACTG`.
# 
# Explain why Hamming distance is unsuitable for one of the pairs.
# 

# In[ ]:


# Write Exercise 3 here.


# ## Exercise 4: enzyme prediction
# 
# Using the estimated \(V_{max}\) and \(K_m\):
# 
# 1. predict the velocity at `[S] = 3 mM`;
# 2. predict the velocity when `[S] = Km`;
# 3. compare the second answer with `Vmax / 2`;
# 4. explain why those two numbers should agree apart from rounding.
# 

# In[ ]:


# Write Exercise 4 here.


# ## Exercise 5: modify and interpret a dataset
# 
# Make a copy of `kinetics_data`. Change the velocity at the smallest substrate concentration from `7.1` to `4.0`. Repeat the Lineweaver–Burk fit and compare the new estimates with the earlier estimates.
# 
# **Question:** Why does changing one low-concentration observation strongly affect the reciprocal fit?
# 

# In[ ]:


# Write Exercise 5 here.


# # Part 7 — Optional extension: a sliding-window GC profile
# 
# A whole sequence can have one GC percentage while different regions have different compositions. A **sliding window** examines one small region at a time.
# 
# For window size 10:
# 
# 1. take bases 0–9;
# 2. calculate their GC percentage;
# 3. move one base forward and take bases 1–10;
# 4. continue until a complete window no longer fits.
# 
# This idea appears in genome scanning, quality control and many time-series analyses.
# 

# In[ ]:


def sliding_gc(sequence, window_size):
    results = []

    last_start = len(sequence) - window_size

    for start in range(last_start + 1):
        end = start + window_size
        window_sequence = sequence[start:end]
        gc_percent = calculate_gc(window_sequence)

        results.append(
            {
                "start": start,
                "end": end,
                "GC_percent": gc_percent,
            }
        )

    return results


window_results = sliding_gc(sequences["isolate_A"], window_size=10)
window_results[:5]


# Python slicing excludes the ending position. Therefore, `sequence[start:end]` includes `start` but stops before `end`. With `start = 0` and `end = 10`, ten characters are selected: positions 0 through 9.
# 

# In[ ]:


window_table = pd.DataFrame(window_results)

plt.figure(figsize=(8, 4))
plt.plot(window_table["start"], window_table["GC_percent"], marker="o")
plt.xlabel("Window start position (Python index)")
plt.ylabel("GC percentage")
plt.title("Sliding-window GC profile for isolate_A")
plt.grid(alpha=0.25)
plt.show()


# # Part 8 — Common mistakes and debugging questions
# 
# | Mistake | Likely result | Debugging question |
# |---|---|---|
# | forgetting to clean sequence lines | newline or space counted as sequence characters | Did I use `.strip()`? |
# | not saving the final FASTA record | final sequence missing | What event saves the final record? |
# | starting DP loops at 0 | negative indexes used unexpectedly | Was row 0 already initialised? |
# | using `min()` rather than `max()` for similarity scores | selects the worst candidate | Am I maximising a score or minimising a cost? |
# | dividing by zero in reciprocal data | infinite or error values | Did I check for zeros? |
# | exchanging x and y on Lineweaver–Burk plot | wrong slope interpretation | Is x equal to `1/[S]`? |
# | omitting units | scientifically ambiguous result | Are units shown in tables and axes? |
# | treating fitted values as exact truth | overconfident conclusion | What assumptions and measurement errors remain? |
# 

# # Part 9 — Review questions
# 
# 1. What is an algorithm?
# 2. Why is pseudocode useful before Python code is written?
# 3. Why is a dictionary suitable for storing FASTA records?
# 4. Why must the last FASTA record be saved after the loop?
# 5. In your own words, what is dynamic programming?
# 6. What three edit operations are represented in an edit-distance table?
# 7. Why does a table for sequences of lengths \(m\) and \(n\) require \((m+1)\times(n+1)\) cells?
# 8. What does the bottom-right edit-distance cell contain?
# 9. What is \(V_{max}\)?
# 10. What is the velocity when substrate concentration equals \(K_m\)?
# 11. What are the x- and y-variables in a Lineweaver–Burk plot?
# 12. Why can reciprocal transformation give too much influence to low substrate concentrations?
# 

# # Part 10 — Key terms
# 
# | Term | Beginner-friendly meaning |
# |---|---|
# | algorithm | ordered, unambiguous steps for solving a problem |
# | pseudocode | logic written in structured ordinary language |
# | FASTA | text format for labelled biological sequences |
# | prefix | beginning portion of a sequence |
# | dynamic programming | solving and storing smaller overlapping problems to build a larger answer |
# | initialisation | setting starting values before the main calculation |
# | recurrence | rule that calculates a new value from earlier values |
# | Hamming distance | number of mismatches between equal-length sequences |
# | edit distance | minimum number of insertions, deletions and substitutions |
# | parameter | value controlling a model, such as \(V_{max}\) or \(K_m\) |
# | reciprocal | one divided by a value |
# | model | simplified mathematical description of a system |
# | complexity | description of how time or memory requirements grow with input size |
# 

# # Lecture summary
# 
# In this lecture, basic Python components were combined into scientific applications.
# 
# - A FASTA file was parsed into a dictionary and summarised using loops, conditions and functions.
# - Dynamic programming was introduced as a method that stores answers to smaller problems.
# - Hamming distance was used for simple position-by-position comparison.
# - Edit distance was calculated by hand and with a dynamic-programming table in Python.
# - Enzyme-kinetics observations were plotted and interpreted.
# - The Michaelis–Menten equation was translated into a Python function.
# - A Lineweaver–Burk plot was constructed, and \(V_{max}\) and \(K_m\) were estimated.
# - Limitations and assumptions were treated as part of the analysis, not as an afterthought.
# 
# The important skill is not memorising the final code. It is learning how to move from a scientific question, to a clear algorithm, to tested Python code, and finally to a cautious scientific interpretation.
# 
