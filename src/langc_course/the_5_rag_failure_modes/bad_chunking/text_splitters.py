"""
Text Splitters and chunking strategies 
optimizing document chunks for rag 
"""


from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
    Language
)
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()

SAMPLE_TEXT = """
# Introduction to Machine Learning

Machine learning is a subset of artificial intelligence (AI) that focuses on building systems that can learn from data and improve their performance without being explicitly programmed.

Machine learning algorithms identify patterns in data and use these patterns to make predictions, classifications, or decisions.

## Types of Machine Learning

There are three main types of machine learning: supervised learning, unsupervised learning, and reinforcement learning.

### 1. Supervised Learning

Supervised learning is a type of machine learning where a model is trained using labeled data.

Labeled data contains input features and their corresponding correct outputs.

The model learns the relationship between inputs and outputs so it can make predictions on new data.

Examples:
- Predicting house prices.
- Detecting spam emails.
- Predicting student exam results.

Common algorithms include:
- Linear Regression
- Logistic Regression
- Decision Trees
- Random Forest
- Support Vector Machines (SVM)
- Neural Networks

### 2. Unsupervised Learning

Unsupervised learning is a type of machine learning where a model learns from data without labeled outputs.

The objective is to discover hidden patterns, structures, or relationships in the dataset.

Examples:
- Customer segmentation.
- Grouping similar documents.
- Detecting unusual behavior.

Common algorithms include:
- K-Means Clustering
- Hierarchical Clustering
- DBSCAN
- Principal Component Analysis (PCA)

### 3. Reinforcement Learning

Reinforcement learning is a type of machine learning where an agent learns by interacting with an environment.

The agent performs actions and receives rewards or penalties based on its behavior.

The objective is to learn a strategy that maximizes the total reward over time.

Examples:
- Training robots.
- Developing game-playing agents.
- Autonomous navigation.

Common algorithms include:
- Q-Learning
- Deep Q-Networks (DQN)
- Policy Gradient Methods

## Applications of Machine Learning

Machine learning is used in various applications, including:

- Image recognition: Identifying objects and faces in images.
- Natural Language Processing: Understanding and processing human language.
- Recommendation Systems: Suggesting products, movies, or music.
- Healthcare: Supporting medical image analysis and prediction.
- Finance: Detecting fraudulent transactions.
- Transportation: Supporting autonomous driving systems.

## Advantages of Machine Learning

- Automates complex tasks.
- Identifies patterns in large datasets.
- Improves predictions as models learn from more data.
- Supports data-driven decision-making.

## Challenges of Machine Learning

- Requires sufficient and relevant training data.
- Models can inherit biases from their training data.
- Training complex models can require significant computing resources.
- Some models are difficult to interpret.
"""




SIMPLE_CODE = """
# Simple Machine Learning Example: Linear Regression

from sklearn.linear_model import LinearRegression

# Training data
X = [[1], [2], [3], [4], [5]]
y = [2, 4, 6, 8, 10]

# Create the model
model = LinearRegression()

# Train the model
model.fit(X, y)

# Make a prediction
prediction = model.predict([[6]])

print("Prediction:", prediction[0])
"""  



def recursive_splitter():
    """
    Recursive Character Text Splitter
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks= splitter.split_text(SAMPLE_TEXT)
    print(f"Original text length: {len(SAMPLE_TEXT)}")
    print(f"Number of chunks created: {len(chunks)}")
    print(f"Chunk sizes: {[len(chunk) for chunk in chunks]}")
    print(f"First chunk: {chunks[0][:200]}...")  # Print first 200 characters of the first chunk





if __name__ == "__main__":
    print("=== Recursive Character Text Splitter ===")
    recursive_splitter()
