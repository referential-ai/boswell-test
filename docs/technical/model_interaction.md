# Model Interaction Diagram

This document visualizes how models interact within the Boswell Test framework.

## Boswell Test Workflow

The diagram below illustrates the process flow of the Boswell Test, showing how models generate essays, grade each other's work, and how the system analyzes the results.

```mermaid
flowchart TD
    subgraph Initialization
        A[Select Domain & Models] --> B[Verify Models]
        B --> C[Prepare Test Environment]
    end

    subgraph Essay Generation
        C --> D1[Model 1 generates essay]
        C --> D2[Model 2 generates essay]
        C --> D3[Model 3 generates essay]
        C --> Dn[Model n generates essay]
    end

    subgraph Peer Grading
        D1 --> E1[Essays Pool]
        D2 --> E1
        D3 --> E1
        Dn --> E1
        
        E1 --> F1[Model 1 grades other essays]
        E1 --> F2[Model 2 grades other essays]
        E1 --> F3[Model 3 grades other essays]
        E1 --> Fn[Model n grades other essays]
    end

    subgraph Analysis
        F1 --> G[Collect All Grades]
        F2 --> G
        F3 --> G
        Fn --> G
        
        G --> H1[Calculate Performance Scores]
        G --> H2[Analyze Grading Bias]
        G --> H3[Measure Response Times]
        G --> H4[Evaluate Empathy]

        H1 --> I[Calculate Boswell Quotient]
        H2 --> I
        H3 --> I
        H4 --> I
    end

    subgraph Reporting
        I --> J1[Generate Visualizations]
        I --> J2[Create Grade Tables]
        I --> J3[Save Individual Essays]
        I --> J4[Compile Summary Reports]
        
        J1 --> K[Complete Results Directory]
        J2 --> K
        J3 --> K
        J4 --> K
    end

    classDef model fill:#226699,stroke:#fff,stroke-width:3px,color:#fff,font-weight:bold
    classDef data fill:#884488,stroke:#fff,stroke-width:2px,color:#fff,font-weight:bold
    classDef process fill:#66BB66,stroke:#fff,stroke-width:2px,color:#fff,font-weight:bold
    
    class D1,D2,D3,Dn,F1,F2,F3,Fn model
    class E1,G,K data
    class H1,H2,H3,H4,I process
```

## Model Interaction Detail

This diagram shows the interactions between specific models in a test scenario, illustrating the peer review process.

```mermaid
flowchart LR
    subgraph Domain[Domain: Political Science]
        Prompt[Essay Prompt]
    end

    subgraph Models
        M1[GPT-4o]
        M2[Claude-3.7-Sonnet]
        M3[Llama-3-8B]
        M4[Perplexity-70B]
    end

    subgraph Essays
        E1[Essay by GPT-4o]
        E2[Essay by Claude-3.7-Sonnet]
        E3[Essay by Llama-3-8B]
        E4[Essay by Perplexity-70B]
    end

    subgraph Grading
        G12[GPT-4o → B+]
        G13[GPT-4o → A-]
        G14[GPT-4o → B]
        
        G21[Claude-3.7-Sonnet → A]
        G23[Claude-3.7-Sonnet → B]
        G24[Claude-3.7-Sonnet → B+]
        
        G31[Llama-3-8B → A-]
        G32[Llama-3-8B → B+]
        G34[Llama-3-8B → C+]
        
        G41[Perplexity-70B → A]
        G42[Perplexity-70B → A-]
        G43[Perplexity-70B → B+]
    end

    subgraph Analysis
        Perf[Performance Scores]
        Bias[Grading Bias Analysis]
        Time[Timing Analysis]
        Emp[Empathy Evaluation]
        BQ[Boswell Quotient]
    end

    Domain --> Models
    Prompt --> Models
    
    Models --> Essays
    M1 --> E1
    M2 --> E2
    M3 --> E3
    M4 --> E4
    
    E2 --> G12
    E3 --> G13
    E4 --> G14
    
    E1 --> G21
    E3 --> G23
    E4 --> G24
    
    E1 --> G31
    E2 --> G32
    E4 --> G34
    
    E1 --> G41
    E2 --> G42
    E3 --> G43
    
    G12 --> E2
    G13 --> E3
    G14 --> E4
    
    G21 --> E1
    G23 --> E3
    G24 --> E4
    
    G31 --> E1
    G32 --> E2
    G34 --> E4
    
    G41 --> E1
    G42 --> E2
    G43 --> E3
    
    E1 --> Perf
    E2 --> Perf
    E3 --> Perf
    E4 --> Perf
    
    G12 --> Bias
    G13 --> Bias
    G14 --> Bias
    G21 --> Bias
    G23 --> Bias
    G24 --> Bias
    G31 --> Bias
    G32 --> Bias
    G34 --> Bias
    G41 --> Bias
    G42 --> Bias
    G43 --> Bias
    
    Perf --> BQ
    Bias --> BQ
    Time --> BQ
    Emp --> BQ

    classDef modelNode fill:#226699,stroke:#fff,stroke-width:3px,color:#fff,font-weight:bold
    classDef essayNode fill:#884488,stroke:#fff,stroke-width:2px,color:#fff,font-weight:bold
    classDef gradeNode fill:#F9A03F,stroke:#fff,stroke-width:2px,color:#000,font-weight:bold
    classDef analysisNode fill:#66BB66,stroke:#fff,stroke-width:2px,color:#fff,font-weight:bold
    
    class M1,M2,M3,M4 modelNode
    class E1,E2,E3,E4 essayNode
    class G12,G13,G14,G21,G23,G24,G31,G32,G34,G41,G42,G43 gradeNode
    class Perf,Bias,Time,Emp,BQ analysisNode
```

## Boswell Quotient Calculation

This diagram illustrates how the Boswell Quotient is calculated from the four component scores.

```mermaid
flowchart TD
    subgraph Components
        P[Performance Score]
        E[Evaluation Score]
        Ef[Efficiency Score]
        Em[Empathy Score]
    end
    
    subgraph Calculation
        W1[Weight: 25%]
        W2[Weight: 25%]
        W3[Weight: 25%]
        W4[Weight: 25%]
        
        P --> |×| W1
        E --> |×| W2
        Ef --> |×| W3
        Em --> |×| W4
        
        W1 --> Sum
        W2 --> Sum
        W3 --> Sum
        W4 --> Sum
        Sum[Sum of Weighted Scores]
    end
    
    Sum --> BQ[Boswell Quotient]
    BQ --> Grade[Letter Grade]
    
    classDef componentNode fill:#226699,stroke:#fff,stroke-width:3px,color:#fff,font-weight:bold
    classDef weightNode fill:#884488,stroke:#fff,stroke-width:2px,color:#fff,font-weight:bold
    classDef resultNode fill:#66BB66,stroke:#fff,stroke-width:2px,color:#fff,font-weight:bold
    
    class P,E,Ef,Em componentNode
    class W1,W2,W3,W4 weightNode
    class Sum,BQ,Grade resultNode
```

These diagrams provide a visual representation of how models interact in the Boswell Test framework, illustrating the peer review process and result calculation methods.