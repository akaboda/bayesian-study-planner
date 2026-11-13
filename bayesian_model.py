
from pgmpy.models import DiscreteBayesianNetwork

# Create the Bayesian network and define its relationships
model = DiscreteBayesianNetwork([
    ("AlgebraDifficulty", "AlgebraMastery"),
    ("CalculusDifficulty", "CalculusMastery"),
    ("StatisticsDifficulty", "StatisticsMastery"),

    ("AlgebraMastery", "StudyNeed"),
    ("CalculusMastery", "StudyNeed"),
    ("StatisticsMastery", "StudyNeed"),
    ("ExamProximity", "StudyNeed"),
    ("StressLevel", "StudyNeed")
])

# Display the variables and relationships
print("Variables:", list(model.nodes()))
print("Relationships:", list(model.edges()))


from pgmpy.factors.discrete import TabularCPD

# Prior probabilities for concept difficulty

algebra_difficulty_cpd = TabularCPD(
    variable="AlgebraDifficulty",
    variable_card=2,
    values=[[0.60], [0.40]],
    state_names={"AlgebraDifficulty": ["Easy", "Hard"]}
)

calculus_difficulty_cpd = TabularCPD(
    variable="CalculusDifficulty",
    variable_card=2,
    values=[[0.30], [0.70]],
    state_names={"CalculusDifficulty": ["Easy", "Hard"]}
)

statistics_difficulty_cpd = TabularCPD(
    variable="StatisticsDifficulty",
    variable_card=2,
    values=[[0.50], [0.50]],
    state_names={"StatisticsDifficulty": ["Easy", "Hard"]}
)

# Add the three CPTs to our network
model.add_cpds(
    algebra_difficulty_cpd,
    calculus_difficulty_cpd,
    statistics_difficulty_cpd
)

print("\nAlgebra Difficulty CPT:")
print(algebra_difficulty_cpd)


# Conditional probability tables for concept mastery

algebra_mastery_cpd = TabularCPD(
    variable="AlgebraMastery",
    variable_card=2,
    values=[
        [0.20, 0.70],  # P(Low Mastery | Easy, Hard)
        [0.80, 0.30]   # P(High Mastery | Easy, Hard)
    ],
    evidence=["AlgebraDifficulty"],
    evidence_card=[2],
    state_names={
        "AlgebraMastery": ["Low", "High"],
        "AlgebraDifficulty": ["Easy", "Hard"]
    }
)

calculus_mastery_cpd = TabularCPD(
    variable="CalculusMastery",
    variable_card=2,
    values=[
        [0.25, 0.80],
        [0.75, 0.20]
    ],
    evidence=["CalculusDifficulty"],
    evidence_card=[2],
    state_names={
        "CalculusMastery": ["Low", "High"],
        "CalculusDifficulty": ["Easy", "Hard"]
    }
)

statistics_mastery_cpd = TabularCPD(
    variable="StatisticsMastery",
    variable_card=2,
    values=[
        [0.15, 0.65],
        [0.85, 0.35]
    ],
    evidence=["StatisticsDifficulty"],
    evidence_card=[2],
    state_names={
        "StatisticsMastery": ["Low", "High"],
        "StatisticsDifficulty": ["Easy", "Hard"]
    }
)

model.add_cpds(
    algebra_mastery_cpd,
    calculus_mastery_cpd,
    statistics_mastery_cpd
)

print("\nAlgebra Mastery CPT:")
print(algebra_mastery_cpd)


# Prior probabilities for exam proximity

exam_proximity_cpd = TabularCPD(
    variable="ExamProximity",
    variable_card=2,
    values=[[0.50], [0.50]],
    state_names={"ExamProximity": ["Soon", "Later"]}
)

# Prior probabilities for student stress

stress_level_cpd = TabularCPD(
    variable="StressLevel",
    variable_card=2,
    values=[[0.50], [0.50]],
    state_names={"StressLevel": ["Low", "High"]}
)

# Add both CPTs to the network
model.add_cpds(
    exam_proximity_cpd,
    stress_level_cpd
)

print("\nExam Proximity CPT:")
print(exam_proximity_cpd)

print("\nStress Level CPT:")
print(stress_level_cpd)


from itertools import product

# Parent variables of StudyNeed, in a fixed order
parents = [
    "AlgebraMastery",
    "CalculusMastery",
    "StatisticsMastery",
    "ExamProximity",
    "StressLevel"
]

# Generate every combination of the five binary parent variables
combinations = list(product([0, 1], repeat=5))

high_need_probs = []
low_need_probs = []

for a, c, s, e, t in combinations:
    # Mastery: 0 = Low, 1 = High
    # Exam proximity: 0 = Soon, 1 = Later
    # Stress: 0 = Low, 1 = High

    p_high = (
        0.10
        + 0.15 * (a == 0)
        + 0.20 * (c == 0)
        + 0.15 * (s == 0)
        + 0.20 * (e == 0)
        + 0.10 * (t == 1)
    )

    high_need_probs.append(p_high)
    low_need_probs.append(1 - p_high)

# Create the StudyNeed CPT
study_need_cpd = TabularCPD(
    variable="StudyNeed",
    variable_card=2,
    values=[low_need_probs, high_need_probs],
    evidence=parents,
    evidence_card=[2] * 5,
    state_names={
        "StudyNeed": ["Low", "High"],
        "AlgebraMastery": ["Low", "High"],
        "CalculusMastery": ["Low", "High"],
        "StatisticsMastery": ["Low", "High"],
        "ExamProximity": ["Soon", "Later"],
        "StressLevel": ["Low", "High"]
    }
)

model.add_cpds(study_need_cpd)

print("\nStudy Need CPT created!")
print("Number of parent combinations:", len(combinations))
print("Network valid:", model.check_model())
