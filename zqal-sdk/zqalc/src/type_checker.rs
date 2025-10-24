use std::collections::HashMap;
use anyhow::{Result, anyhow};

use crate::ast::{Ast, Function, FunctionKind, QuantumDecl, ToneDecl, Span};

#[derive(Debug, Clone, PartialEq)]
pub enum Type {
    U32,
    U64,
    F64,
    Bool,
    Hash32,
    Bytes80,
    Array(Box<Type>, usize),
    QuantumArray(Box<Type>, usize),
    Void,
}

#[derive(Debug)]
pub struct TypeError {
    pub message: String,
    pub span: Span,
}

pub struct TypeChecker {
    errors: Vec<TypeError>,
    symbol_table: HashMap<String, Type>,
    function_table: HashMap<String, FunctionType>,
}

#[derive(Debug, Clone)]
pub struct FunctionType {
    pub params: Vec<(String, Type)>,
    pub return_type: Type,
    pub kind: FunctionKind,
}

impl TypeChecker {
    pub fn new() -> Self {
        let mut symbol_table = HashMap::new();
        let mut function_table = HashMap::new();

        // Add built-in types and functions
        Self::add_builtins(&mut symbol_table, &mut function_table);

        Self {
            errors: Vec::new(),
            symbol_table,
            function_table,
        }
    }

    fn add_builtins(symbols: &mut HashMap<String, Type>, functions: &mut HashMap<String, FunctionType>) {
        // Built-in quantum functions
        functions.insert("entangle".to_string(), FunctionType {
            params: vec![
                ("a".to_string(), Type::U32),
                ("b".to_string(), Type::U32),
            ],
            return_type: Type::U32,
            kind: FunctionKind::Kernel,
        });

        functions.insert("collapse".to_string(), FunctionType {
            params: vec![
                ("state".to_string(), Type::Array(Box::new(Type::U32), 12)),
            ],
            return_type: Type::U32,
            kind: FunctionKind::Kernel,
        });

        functions.insert("superpose".to_string(), FunctionType {
            params: vec![
                ("state".to_string(), Type::U32),
            ],
            return_type: Type::U32,
            kind: FunctionKind::Kernel,
        });

        functions.insert("measure".to_string(), FunctionType {
            params: vec![
                ("state".to_string(), Type::U32),
            ],
            return_type: Type::Bool,
            kind: FunctionKind::Kernel,
        });

        // Tone functions
        functions.insert("apply_tone".to_string(), FunctionType {
            params: vec![
                ("tone_id".to_string(), Type::U32),
                ("data".to_string(), Type::Array(Box::new(Type::U32), 12)),
            ],
            return_type: Type::Array(Box::new(Type::U32), 12),
            kind: FunctionKind::Kernel,
        });

        // Hash functions
        functions.insert("hash".to_string(), FunctionType {
            params: vec![
                ("data".to_string(), Type::Array(Box::new(Type::U32), 12)),
            ],
            return_type: Type::Hash32,
            kind: FunctionKind::Kernel,
        });
    }

    pub fn check(&mut self, ast: &Ast) -> Result<()> {
        // Check algorithm
        if let Some(algorithm) = &ast.algorithm {
            self.check_algorithm(algorithm)?;
        }

        // Check quantum declarations
        for quantum in &ast.quantum {
            self.check_quantum_decl(quantum)?;
        }

        // Check tone declarations
        for tone in &ast.tones {
            self.check_tone_decl(tone)?;
        }

        // Check functions
        for function in &ast.functions {
            self.check_function(function)?;
        }

        if self.errors.is_empty() {
            Ok(())
        } else {
            let error_messages: Vec<String> = self.errors.iter()
                .map(|e| format!("Type error: {}", e.message))
                .collect();
            Err(anyhow!("Type checking failed:\n{}", error_messages.join("\n")))
        }
    }

    fn check_algorithm(&mut self, algorithm: &crate::ast::Algorithm) -> Result<()> {
        // Basic algorithm validation
        if algorithm.name.is_empty() {
            self.errors.push(TypeError {
                message: "Algorithm name cannot be empty".to_string(),
                span: algorithm.span.clone(),
            });
        }
        Ok(())
    }

    fn check_quantum_decl(&mut self, quantum: &QuantumDecl) -> Result<()> {
        // Parse quantum type
        let ty = self.parse_type(&quantum.ty)?;
        let quantum_type = Type::QuantumArray(Box::new(ty), quantum.size as usize);

        // Check for duplicate declarations
        if self.symbol_table.contains_key(&quantum.name) {
            self.errors.push(TypeError {
                message: format!("Quantum variable '{}' already declared", quantum.name),
                span: quantum.span.clone(),
            });
        } else {
            self.symbol_table.insert(quantum.name.clone(), quantum_type);
        }

        Ok(())
    }

    fn check_tone_decl(&mut self, tone: &ToneDecl) -> Result<()> {
        // Validate tone ID range
        if tone.id == 0 || tone.id > 70 {
            self.errors.push(TypeError {
                message: format!("Invalid tone ID: {}. Must be between 1-70", tone.id),
                span: tone.span.clone(),
            });
        }
        Ok(())
    }

    fn check_function(&mut self, function: &Function) -> Result<()> {
        // Parse return type
        let return_type = if let Some(ref rt) = function.return_type {
            self.parse_type(rt)?
        } else {
            Type::Void
        };

        // Create function type
        let func_type = FunctionType {
            params: Vec::new(), // TODO: parse parameters
            return_type,
            kind: function.kind.clone(),
        };

        // Check for duplicate function declarations
        if self.function_table.contains_key(&function.name) {
            self.errors.push(TypeError {
                message: format!("Function '{}' already declared", function.name),
                span: function.span.clone(),
            });
        } else {
            self.function_table.insert(function.name.clone(), func_type);
        }

        Ok(())
    }

    fn parse_type(&self, type_str: &str) -> Result<Type> {
        match type_str {
            "u32" => Ok(Type::U32),
            "u64" => Ok(Type::U64),
            "f64" => Ok(Type::F64),
            "bool" => Ok(Type::Bool),
            "hash32" => Ok(Type::Hash32),
            "bytes80" => Ok(Type::Bytes80),
            _ => {
                // Try to parse array types like [u32; 12]
                if type_str.starts_with('[') && type_str.ends_with(']') {
                    let inner = &type_str[1..type_str.len()-1];
                    if let Some(semicolon_pos) = inner.rfind(';') {
                        let element_type_str = &inner[..semicolon_pos];
                        let size_str = &inner[semicolon_pos+1..];
                        let element_type = self.parse_type(element_type_str.trim())?;
                        let size = size_str.trim().parse::<usize>()?;
                        return Ok(Type::Array(Box::new(element_type), size));
                    }
                }
                Err(anyhow!("Unknown type: {}", type_str))
            }
        }
    }

    pub fn get_errors(&self) -> &[TypeError] {
        &self.errors
    }
}