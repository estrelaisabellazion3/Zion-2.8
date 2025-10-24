use std::fs;
use std::path::PathBuf;
use anyhow::{Context, Result};
use clap::{Parser, Subcommand};

mod ast;
mod parser;

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
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    match cli.command {
        Commands::Parse { file } => parse_cmd(file),
        Commands::Tokens { file } => tokens_cmd(file),
        Commands::Ast { file } => ast_cmd(file),
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
