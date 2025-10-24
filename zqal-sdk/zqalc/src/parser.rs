use anyhow::Result;
use regex::Regex;

use crate::ast::{Algorithm, Ast, Function, FunctionKind, QuantumDecl, ToneDecl};

pub fn build_ast(src: &str) -> Result<Ast> {
    let mut algorithm: Option<Algorithm> = None;
    let mut functions: Vec<Function> = Vec::new();
    let mut quantum: Vec<QuantumDecl> = Vec::new();
    let mut tones: Vec<ToneDecl> = Vec::new();

    // Algorithm name
    if let Some(cap) = Regex::new(r"@algorithm\s+([A-Za-z_][A-Za-z0-9_]*)")?
        .captures(src)
    {
        algorithm = Some(Algorithm {
            name: cap.get(1).unwrap().as_str().to_string(),
        });
    }

    // Functions
    let fn_kinds: Vec<(FunctionKind, Regex)> = vec![
        (FunctionKind::Kernel, Regex::new(r"@kernel\s+fn\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")),
        (FunctionKind::Validator, Regex::new(r"@validator\s+fn\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")),
        (FunctionKind::Reward, Regex::new(r"@reward\s+fn\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")),
    ]
    .into_iter()
    .map(|(k, r)| r.map(|re| (k, re)))
    .collect::<Result<Vec<_>, _>>()?;
    for (kind, re) in fn_kinds {
        for caps in re.captures_iter(src) {
            let name = caps.get(1).unwrap().as_str().to_string();
            functions.push(Function {
                kind: match kind {
                    FunctionKind::Kernel => FunctionKind::Kernel,
                    FunctionKind::Validator => FunctionKind::Validator,
                    FunctionKind::Reward => FunctionKind::Reward,
                },
                name,
                return_type: None,
            });
        }
    }

    // Quantum declarations
    let re = Regex::new(r"quantum\s+([A-Za-z_][A-Za-z0-9_]*)\[(\d+)\]\s*:\s*([^;\n]+)")?;
    for caps in re.captures_iter(src) {
        let name = caps.get(1).unwrap().as_str().to_string();
        let size: u32 = caps.get(2).unwrap().as_str().parse().unwrap_or(0);
        let ty = caps.get(3).unwrap().as_str().trim().to_string();
        quantum.push(QuantumDecl { name, size, ty });
    }

    // Tone declarations (@tone N)
    for caps in Regex::new(r"@tone\s+(\d+)")?.captures_iter(src) {
        let id: u32 = caps.get(1).unwrap().as_str().parse().unwrap_or(0);
        tones.push(ToneDecl { id });
    }

    Ok(Ast {
        algorithm,
        functions,
        quantum,
        tones,
    })
}
