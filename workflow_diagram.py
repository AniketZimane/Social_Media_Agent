import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_workflow_diagram():
    """Create interactive workflow diagram"""
    
    fig = go.Figure()
    
    # Define workflow steps
    steps = [
        {"name": "User Input", "x": 1, "y": 8, "color": "#FF6B6B"},
        {"name": "Topic Analysis", "x": 3, "y": 8, "color": "#4ECDC4"},
        {"name": "Platform Selection", "x": 5, "y": 8, "color": "#45B7D1"},
        {"name": "AI Processing", "x": 7, "y": 8, "color": "#96CEB4"},
        {"name": "Content Generation", "x": 9, "y": 8, "color": "#FFEAA7"},
        
        # AI Services
        {"name": "Google AI\n(Gemini)", "x": 6, "y": 6, "color": "#DDA0DD"},
        {"name": "Replicate\n(Llama-2)", "x": 8, "y": 6, "color": "#DDA0DD"},
        {"name": "Free AI\n(Fallback)", "x": 10, "y": 6, "color": "#DDA0DD"},
        
        # Output Components
        {"name": "Blog Content", "x": 3, "y": 4, "color": "#FFB6C1"},
        {"name": "Hashtags", "x": 5, "y": 4, "color": "#FFB6C1"},
        {"name": "Images", "x": 7, "y": 4, "color": "#FFB6C1"},
        {"name": "SEO Keywords", "x": 9, "y": 4, "color": "#FFB6C1"},
        
        # Analytics
        {"name": "Engagement\nPrediction", "x": 2, "y": 2, "color": "#98FB98"},
        {"name": "Platform\nOptimization", "x": 4, "y": 2, "color": "#98FB98"},
        {"name": "Trending\nAnalysis", "x": 6, "y": 2, "color": "#98FB98"},
        {"name": "Content\nCalendar", "x": 8, "y": 2, "color": "#98FB98"},
        
        # Final Output
        {"name": "Complete Blog Package", "x": 5, "y": 0.5, "color": "#FFD700"}
    ]
    
    # Add nodes
    for step in steps:
        fig.add_trace(go.Scatter(
            x=[step["x"]], 
            y=[step["y"]], 
            mode='markers+text',
            marker=dict(size=40, color=step["color"], line=dict(width=2, color='white')),
            text=step["name"],
            textposition="middle center",
            textfont=dict(size=10, color='black'),
            showlegend=False,
            hovertemplate=f"<b>{step['name']}</b><extra></extra>"
        ))
    
    # Add arrows (connections)
    arrows = [
        # Main workflow
        (1, 8, 3, 8), (3, 8, 5, 8), (5, 8, 7, 8), (7, 8, 9, 8),
        
        # AI Services connections
        (7, 8, 6, 6), (7, 8, 8, 6), (7, 8, 10, 6),
        
        # Output connections
        (9, 8, 3, 4), (9, 8, 5, 4), (9, 8, 7, 4), (9, 8, 9, 4),
        
        # Analytics connections
        (3, 4, 2, 2), (5, 4, 4, 2), (7, 4, 6, 2), (9, 4, 8, 2),
        
        # Final output
        (2, 2, 5, 0.5), (4, 2, 5, 0.5), (6, 2, 5, 0.5), (8, 2, 5, 0.5)
    ]
    
    for x1, y1, x2, y2 in arrows:
        fig.add_annotation(
            x=x2, y=y2, ax=x1, ay=y1,
            xref='x', yref='y', axref='x', ayref='y',
            arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='gray'
        )
    
    # Update layout
    fig.update_layout(
        title="🤖 Agentic AI Blog Writing Assistant - Workflow Diagram",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 11]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 9]),
        plot_bgcolor='white',
        height=600,
        width=1000
    )
    
    return fig

def create_data_flow_diagram():
    """Create data flow diagram"""
    
    fig = go.Figure()
    
    # Data sources
    sources = [
        {"name": "User Input\n(Topic + Platform)", "x": 2, "y": 7, "color": "#FF6B6B"},
        {"name": "Google AI API", "x": 6, "y": 7, "color": "#4285F4"},
        {"name": "Replicate API", "x": 10, "y": 7, "color": "#FF4081"},
        {"name": "RAG Knowledge\nBase", "x": 2, "y": 5, "color": "#9C27B0"},
        {"name": "Free APIs\n(Unsplash, Reddit)", "x": 6, "y": 5, "color": "#FF9800"},
        {"name": "Smart Algorithms", "x": 10, "y": 5, "color": "#4CAF50"}
    ]
    
    # Processing layers
    processing = [
        {"name": "Content Fusion\nEngine", "x": 4, "y": 3, "color": "#2196F3"},
        {"name": "Engagement\nPredictor", "x": 8, "y": 3, "color": "#E91E63"}
    ]
    
    # Outputs
    outputs = [
        {"name": "Blog Content", "x": 2, "y": 1, "color": "#FFB6C1"},
        {"name": "Hashtags", "x": 4, "y": 1, "color": "#FFB6C1"},
        {"name": "Images", "x": 6, "y": 1, "color": "#FFB6C1"},
        {"name": "Analytics", "x": 8, "y": 1, "color": "#FFB6C1"},
        {"name": "SEO Data", "x": 10, "y": 1, "color": "#FFB6C1"}
    ]
    
    all_nodes = sources + processing + outputs
    
    # Add all nodes
    for node in all_nodes:
        fig.add_trace(go.Scatter(
            x=[node["x"]], 
            y=[node["y"]], 
            mode='markers+text',
            marker=dict(size=35, color=node["color"], line=dict(width=2, color='white')),
            text=node["name"],
            textposition="middle center",
            textfont=dict(size=9, color='white'),
            showlegend=False
        ))
    
    # Add data flow arrows
    flows = [
        # Sources to processing
        (2, 7, 4, 3), (6, 7, 4, 3), (10, 7, 4, 3),
        (2, 5, 4, 3), (6, 5, 8, 3), (10, 5, 8, 3),
        
        # Processing to outputs
        (4, 3, 2, 1), (4, 3, 4, 1), (4, 3, 6, 1),
        (8, 3, 8, 1), (8, 3, 10, 1)
    ]
    
    for x1, y1, x2, y2 in flows:
        fig.add_annotation(
            x=x2, y=y2, ax=x1, ay=y1,
            xref='x', yref='y', axref='x', ayref='y',
            arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor='#333'
        )
    
    fig.update_layout(
        title="📊 Data Flow Architecture",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 12]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 8]),
        plot_bgcolor='#f8f9fa',
        height=500
    )
    
    return fig

def show_workflow_page():
    """Display workflow diagrams in Streamlit"""
    
    st.title("🔄 System Workflow & Architecture")
    
    # Workflow Overview
    st.header("📋 Process Flow")
    workflow_fig = create_workflow_diagram()
    st.plotly_chart(workflow_fig, use_container_width=True)
    
    # Data Flow
    st.header("📊 Data Flow Architecture") 
    dataflow_fig = create_data_flow_diagram()
    st.plotly_chart(dataflow_fig, use_container_width=True)
    
    # Process Description
    st.header("🔍 Process Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Input Processing")
        st.write("""
        1. **User Input**: Topic + Platform selection
        2. **Topic Analysis**: AI analyzes content relevance
        3. **Platform Matching**: Optimizes for target platform
        4. **Content Strategy**: Determines best approach
        """)
        
        st.subheader("🤖 AI Integration")
        st.write("""
        - **Google AI (Primary)**: Content generation & analysis
        - **Replicate (Secondary)**: Advanced AI models
        - **Free APIs (Backup)**: Fallback systems
        - **Smart Algorithms**: Local processing
        """)
    
    with col2:
        st.subheader("📝 Content Generation")
        st.write("""
        1. **Blog Content**: 600-800 word articles
        2. **Hashtags**: Platform-specific tags
        3. **Images**: Professional visuals
        4. **SEO Keywords**: Search optimization
        """)
        
        st.subheader("📈 Analytics & Optimization")
        st.write("""
        - **Engagement Prediction**: AI-powered scoring
        - **Platform Optimization**: Best practices
        - **Trending Analysis**: Real-time insights
        - **Content Calendar**: Scheduling recommendations
        """)

if __name__ == "__main__":
    show_workflow_page()