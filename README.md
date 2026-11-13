
# Bayesian Study Planner
COSC 329 - Learning Analytics

## Project Overview

This project aims to develop a personalized study planning system using a Bayesian network and a calendar API.

The system will consider:
- Difficulty of at least three course concepts
- Student mastery of each concept
- Days remaining until an exam
- Current student stress level

The Bayesian network will estimate the student's study needs based on these factors.

The system will then use an expected utility calculation to choose between three actions:
1. Schedule an intense 5-hour study session
2. Schedule a light 1-hour review session
3. Schedule a rest day

The selected action will be integrated with a calendar API to help students organize their study schedules.

## Original Project Plan

1. Review the project requirements and identify the main features.
2. Design a Bayesian network with approximately 10 variables or fewer.
3. Handcraft and document the conditional probability tables (CPTs).
4. Implement the Bayesian network in Python using pgmpy.
5. Define at least three study actions and a utility function.
6. Use Bayesian inference and expected utility to select the best action.
7. Integrate the system with a calendar API.
8. Test the system using different student scenarios.
9. Record a video demonstrating the working features.
10. Complete the documentation, report, and final submission.


## Current Project Status

- Project setup: Complete
- GitHub repository setup: Complete
- Bayesian network design: Complete
- Bayesian network implementation: Complete
- Handcrafted CPT implementation: Complete
- Network validation: Complete (model.check_model() returned True)
- Bayesian inference: Not started
- Utility function: Not started
- Calendar integration: Not started
- Testing: In progress (initial network validation completed)
- Video demonstration: Not started
- Final report: Not started


## Known Bugs

No bugs identified yet.

## Bayesian Network Design

The Bayesian network models a student's study needs across three mathematics concepts: Algebra, Calculus, and Statistics.

### Variables

The network contains nine binary variables:

1. Algebra Difficulty: Easy / Hard
2. Algebra Mastery: Low / High
3. Calculus Difficulty: Easy / Hard
4. Calculus Mastery: Low / High
5. Statistics Difficulty: Easy / Hard
6. Statistics Mastery: Low / High
7. Exam Proximity: Soon / Later
8. Stress Level: Low / High
9. Study Need: Low / High

### Network Relationships

Each concept's difficulty directly influences the student's mastery of that concept.

- Algebra Difficulty -> Algebra Mastery
- Calculus Difficulty -> Calculus Mastery
- Statistics Difficulty -> Statistics Mastery

The three mastery variables, exam proximity, and stress level influence the probability of high study need.

### Initial Handcrafted CPT: Algebra Mastery

| Algebra Difficulty | P(Low Mastery) | P(High Mastery) |
|---|---|---|
| Easy | 0.20 | 0.80 |
| Hard | 0.70 | 0.30 |

These probabilities are manually assigned based on the assumption that students are generally more likely to master easier concepts than harder ones. They are illustrative model parameters, not probabilities learned from student data.


### Handcrafted CPT: Calculus Mastery

| Calculus Difficulty | P(Low Mastery) | P(High Mastery) |
|---|---|---|
| Easy | 0.25 | 0.75 |
| Hard | 0.80 | 0.20 |

The probabilities assume that students are more likely to have low mastery when Calculus concepts are difficult.

### Handcrafted CPT: Statistics Mastery

| Statistics Difficulty | P(Low Mastery) | P(High Mastery) |
|---|---|---|
| Easy | 0.15 | 0.85 |
| Hard | 0.65 | 0.35 |

The probabilities assume that students are more likely to master easier Statistics concepts than harder ones.

All CPT values are handcrafted assumptions rather than probabilities learned from real student data.


### Prior Probability: Exam Proximity

Exam proximity is determined by the number of days remaining until the exam.

- Soon: 3 days or fewer
- Later: More than 3 days

| Exam Proximity | Probability |
|---|---|
| Soon | 0.50 |
| Later | 0.50 |

These are neutral prior probabilities. The actual exam proximity will be calculated from the student's exam date.

### Prior Probability: Stress Level

| Stress Level | Probability |
|---|---|
| Low | 0.50 |
| High | 0.50 |

These probabilities are neutral assumptions. The student will provide their current stress level as an input.


### Handcrafted CPT: Study Need

Study Need has five parent variables:
- Algebra Mastery
- Calculus Mastery
- Statistics Mastery
- Exam Proximity
- Stress Level

Because each parent has two possible states, the Study Need CPT contains 32 parent-state combinations.

To generate these probabilities consistently, the following rule is used:

P(High Study Need) = 0.10 + 0.15A + 0.20C + 0.15S + 0.20E + 0.10T

Where:
- A = 1 if Algebra Mastery is Low, otherwise 0
- C = 1 if Calculus Mastery is Low, otherwise 0
- S = 1 if Statistics Mastery is Low, otherwise 0
- E = 1 if Exam Proximity is Soon, otherwise 0
- T = 1 if Stress Level is High, otherwise 0

P(Low Study Need) = 1 - P(High Study Need)

The baseline probability is 0.10. Low mastery, an approaching exam, and high stress increase the probability of high study need.

Calculus receives a slightly higher weight because the model assumes it requires more preparation.

All probability values are handcrafted assumptions for demonstration purposes. The model is not trained on real student data.

The full 32-column CPT is generated programmatically in `bayesian_model.py` using Python's `itertools.product`. Each conditional probability distribution sums to 1, and the Bayesian network successfully passes `model.check_model()` validation.


### Prior Probabilities: Concept Difficulty

The three concept difficulty variables are root nodes in the Bayesian network and therefore require prior probability distributions.

| Concept | P(Easy) | P(Hard) |
|---|---|---|
| Algebra | 0.60 | 0.40 |
| Calculus | 0.30 | 0.70 |
| Statistics | 0.50 | 0.50 |

These probabilities are handcrafted assumptions for a fictional mathematics course.

Calculus is assumed to be more difficult on average than Algebra and Statistics. The values are not based on empirical student data.

When concept difficulty is provided as an observation, the model uses that information during inference.


## Project File Structure

- `README.md`: Documents the project overview, original plan, Bayesian network design, progress, and known bugs.
- `bayesian_model.py`: Implements the nine-variable Bayesian network, handcrafted CPTs, and model validation using pgmpy.
- `.gitignore`: Prevents temporary Python files, virtual environment files, and sensitive configuration files from being uploaded to GitHub.

Additional files will be documented as they are created.

## Initial Validation

The Bayesian network was implemented using pgmpy.

Initial validation confirmed:
- All 9 variables were created.
- All 8 directed relationships were defined.
- All 9 variables have probability distributions.
- The Study Need CPT contains 32 parent-state combinations.
- `model.check_model()` returned True.

These checks confirm that the network is structurally and probabilistically valid. They do not yet establish that its predictions are accurate or that it behaves as intended in different student scenarios.

Further inference and scenario testing will be completed during development.
