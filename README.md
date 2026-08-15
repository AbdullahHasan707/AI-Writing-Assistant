# AI Writing Assistant: A Mini Grammarly

An interactive web application prototype built for the **KPITB Week 7 Course Project Assignment**. This application leverages state-of-the-art, pre-trained Transformer architectures to deliver real-time spelling/grammar corrections and contextual next-word predictions. 

The application features an intuitive user suggestion interface that allows users to instantly review, accept, or expand their textual content with a single click.

---

## 🚀 Live Deployment
The application is deployed and accessible online:
🔗 **[Insert Your Streamlit Share App Link Here]**

---

## ✨ Features & Rubric Alignment

| Assignment Requirement | Project Implementation | Status |
| :--- | :--- | :--- |
| **1. Text Input Interface** | A responsive `st.text_area` component serving as the central input layer. | ✅ Implemented |
| **2 & 3. Spelling & Grammar** | Real-time sequence analysis powered by a specialized Transformer model. | ✅ Implemented |
| **4. Next-Word Prediction** | Autoregressive generation predicting contextual upcoming tokens. | ✅ Implemented |
| **5. Suggestion Interface** | Visual split panels (`st.success` / `st.error`) with interactive buttons. | ✅ Implemented |
| **Bonus: Multi-Word Generation** | Generates up to 3 distinct next-word token pills simultaneously. | ✅ Implemented |
| **Bonus: Auto-Accept Updates** | Dynamic Python callback state loops that auto-inject selections. | ✅ Implemented |

---

## 🏗️ Architecture Design Report

The system utilizes a decoupled, lightweight runtime architecture optimized for serverless cloud environments (Streamlit Community Cloud).


