use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Ast {
    pub algorithm: Option<Algorithm>,
    pub functions: Vec<Function>,
    pub quantum: Vec<QuantumDecl>,
    pub tones: Vec<ToneDecl>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Algorithm {
    pub name: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Function {
    pub kind: FunctionKind,
    pub name: String,
    pub return_type: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum FunctionKind {
    Kernel,
    Validator,
    Reward,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct QuantumDecl {
    pub name: String,
    pub size: u32,
    pub ty: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ToneDecl {
    pub id: u32,
}
