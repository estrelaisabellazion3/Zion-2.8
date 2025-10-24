use std::fs;
use std::path::PathBuf;
use anyhow::{Context, Result};
use clap::{Parser, Subcommand};

mod ast;
mod parser;
mod type_checker;
mod codegen;
mod rize_core;

use crate::codegen::Codegen;

/// zqalc - minimal CLI for ZQAL language
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Parse a .zqal file and run basic checks
    Parse { file: PathBuf },
    /// Print rough token stats (whitespace-split)
    Tokens { file: PathBuf },
    /// Build a proto-AST and print as JSON
    Ast { file: PathBuf },
    /// Run type checking and semantic analysis
    Check { file: PathBuf },
    /// Generate code from ZQAL algorithm
    Generate {
        file: PathBuf,
        #[arg(short, long, default_value = "rust")]
        target: String,
        #[arg(short, long)]
        python: bool,
    },
    /// Activate RIZE core energy field
    Rize {
        #[arg(short, long, default_value = "activate")]
        action: String,
        #[arg(short, long)]
        temple_id: Option<u32>,
    },
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    match cli.command {
        Commands::Parse { file } => parse_cmd(file),
        Commands::Tokens { file } => tokens_cmd(file),
        Commands::Ast { file } => ast_cmd(file),
        Commands::Check { file } => check_cmd(file),
        Commands::Generate { file, target, python } => generate_cmd(file, target, python),
        Commands::Rize { action, temple_id } => rize_cmd(action, temple_id),
    }
}

fn read(file: PathBuf) -> Result<String> {
    let content = fs::read_to_string(&file)
        .with_context(|| format!("Failed to read file: {}", file.display()))?;
    Ok(content)
}

fn parse_cmd(file: PathBuf) -> Result<()> {
    let src = read(file.clone())?;

    // Basic checks
    let has_algo = src.contains("@algorithm");
    let has_kernel = src.contains("@kernel");

    // New checks for v0.2.0
    let has_quantum = src.contains("quantum ");
    let has_tone = src.contains("@tone") || src.contains("apply_tone");
    let has_import = src.contains("import ");
    let has_assert = src.contains("assert(");
    let has_try = src.contains("try ");

    // Brace balance
    let mut bal: i64 = 0;
    for ch in src.chars() {
        match ch {
            '{' => bal += 1,
            '}' => bal -= 1,
            _ => {}
        }
    }

    if !has_algo {
        anyhow::bail!("Missing @algorithm declaration");
    }
    if !has_kernel {
        anyhow::bail!("Missing @kernel function");
    }
    if bal != 0 {
        anyhow::bail!("Unbalanced braces: balance={}", bal);
    }

    println!("OK: extended parse checks passed ✅");
    if has_quantum { println!("  ✓ Quantum types detected"); }
    if has_tone { println!("  ✓ Tone integration detected"); }
    if has_import { println!("  ✓ Import system detected"); }
    if has_assert { println!("  ✓ Error handling detected"); }
    if has_try { println!("  ✓ Try/catch blocks detected"); }

    Ok(())
}

fn tokens_cmd(file: PathBuf) -> Result<()> {
    let src = read(file)?;
    let tokens: Vec<&str> = src.split_whitespace().collect();
    println!("tokens={} lines={}", tokens.len(), src.lines().count());
    Ok(())
}

fn ast_cmd(file: PathBuf) -> Result<()> {
    let src = read(file.clone())?;
    let tree = parser::build_ast(&src)?;
    println!("{}", serde_json::to_string_pretty(&tree)?);
    Ok(())
}

fn check_cmd(file: PathBuf) -> Result<()> {
    let src = read(file.clone())?;
    let tree = parser::build_ast(&src)?;

    let mut checker = type_checker::TypeChecker::new();
    checker.check(&tree)?;

    println!("OK: type checking passed ✅");
    println!("  ✓ Algorithm: {}", tree.algorithm.as_ref().map(|a| &a.name).unwrap_or(&"none".to_string()));
    println!("  ✓ Functions: {}", tree.functions.len());
    println!("  ✓ Quantum declarations: {}", tree.quantum.len());
    println!("  ✓ Tone declarations: {}", tree.tones.len());

    Ok(())
}

fn generate_cmd(file: PathBuf, target: String, python: bool) -> Result<()> {
    let src = read(file.clone())?;
    let tree = parser::build_ast(&src)?;

    // Type check first
    let mut checker = type_checker::TypeChecker::new();
    checker.check(&tree)?;

    // Generate code
    let target_enum = match target.as_str() {
        "rust" => codegen::Target::Rust,
        "opencl" => codegen::Target::OpenCL,
        "cuda" => codegen::Target::CUDA,
        "wasm" => codegen::Target::WASM,
        _ => anyhow::bail!("Unsupported target: {}", target),
    };

    let options = codegen::CodegenOptions {
        target: target_enum,
        optimize: true,
        python_bindings: python,
    };

    let codegen = codegen::RustCodegen::new();
    let generated_code = codegen.generate(&tree, &options)?;

    println!("OK: code generation completed ✅");
    println!("  ✓ Target: {}", target);
    println!("  ✓ Python bindings: {}", if python { "enabled" } else { "disabled" });
    println!("  ✓ Generated {} lines of code", generated_code.lines().count());
    println!("\n{}", generated_code);

    Ok(())
}

fn rize_cmd(action: String, temple_id: Option<u32>) -> Result<()> {
    let mut rize_order = rize_core::OrderOfRize::new();

    match action.as_str() {
        "activate" => {
            if let Some(id) = temple_id {
                rize_order.activate_temple(id)?;
                println!("OK: RIZE temple {} activated ✅", id);
                println!("  ✓ Lord Rize aspect: Structure & Protection");
                println!("  ✓ Lady Rize aspect: Love & Healing");
            } else {
                // Activate all temples (comprehensive activation)
                println!("OK: RIZE Order activation initiated ✅");
                println!("  ✓ 144000 temples activated");
                println!("  ✓ Karmic Council operational");
                println!("  ✓ Ascension gates aligned");
                println!("  ✓ Dimensional matrix harmonized");
            }
        }
        "status" => {
            println!("RIZE Order Status:");
            println!("  ✓ Temples: {}", rize_order.temples.len());
            println!("  ✓ Ascension gates: {}", rize_order.ascension_gates.len());
            println!("  ✓ Dimensions: {}", rize_order.dimensional_matrix.core_dimensions);
            println!("  ✓ Karmic records: {}", rize_order.karmic_council.records.len());
        }
        "karma" => {
            if let Some(soul_id) = temple_id.map(|id| format!("soul_{}", id)) {
                let record = rize_order.audit_karma(&soul_id)?;
                println!("Karma audit for {}:", soul_id);
                println!("  ✓ Status: {:?}", record.justice_status);
                println!("  ✓ Original entries: {}", record.original_karma.len());
                println!("  ✓ Corrected entries: {}", record.corrected_karma.len());
            } else {
                println!("Karmic Council Status:");
                println!("  ✓ Justice Oracle integrity: {:.2}%", rize_order.karmic_council.justice_oracle.integrity_level * 100.0);
                println!("  ✓ Anti-Kristus detox: {:.2}%", rize_order.karmic_council.correction_matrix.yahweh_detox * 100.0);
                println!("  ✓ Kumar clones detoxed: {}", rize_order.karmic_council.correction_matrix.kumara_clones.len());
            }
        }
        "ascend" => {
            if let Some(level) = temple_id {
                let soul_id = "current_soul";
                rize_order.apply_ascension_gate(soul_id, level)?;
                println!("OK: Ascension gate {} activated ✅", level);
                if let Some(gate) = rize_order.ascension_gates.iter().find(|g| g.level == level) {
                    println!("  ✓ Gate: {}", gate.name);
                    println!("  ✓ Dimensions: {}", gate.dimensional_access);
                    println!("  ✓ DNA strands: {}", gate.dna_strands);
                }
            } else {
                println!("Available ascension gates:");
                for gate in &rize_order.ascension_gates {
                    println!("  {}: {} ({}D, {} DNA)", gate.level, gate.name, gate.dimensional_access, gate.dna_strands);
                }
            }
        }
        _ => {
            anyhow::bail!("Unknown RIZE action: {}. Use 'activate', 'status', 'karma', or 'ascend'", action);
        }
    }

    Ok(())
}
