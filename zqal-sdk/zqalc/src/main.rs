use std::fs;
use std::path::PathBuf;
use anyhow::{Context, Result};
use clap::{Parser, Subcommand};

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
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    match cli.command {
        Commands::Parse { file } => parse_cmd(file),
        Commands::Tokens { file } => tokens_cmd(file),
    }
}

fn read(file: PathBuf) -> Result<String> {
    let content = fs::read_to_string(&file)
        .with_context(|| format!("Failed to read file: {}", file.display()))?;
    Ok(content)
}

fn parse_cmd(file: PathBuf) -> Result<()> {
    let src = read(file.clone())?;
    // Minimal sanity checks: contains @algorithm and at least one @kernel
    let has_algo = src.contains("@algorithm");
    let has_kernel = src.contains("@kernel");
    if !has_algo {
        anyhow::bail!("Missing @algorithm declaration");
    }
    if !has_kernel {
        anyhow::bail!("Missing @kernel function");
    }
    // A naive brace balance check
    let mut bal: i64 = 0;
    for ch in src.chars() {
        match ch {
            '{' => bal += 1,
            '}' => bal -= 1,
            _ => {}
        }
    }
    if bal != 0 {
        anyhow::bail!("Unbalanced braces: balance={}", bal);
    }
    println!("OK: basic parse checks passed ✅");
    Ok(())
}

fn tokens_cmd(file: PathBuf) -> Result<()> {
    let src = read(file)?;
    let tokens: Vec<&str> = src.split_whitespace().collect();
    println!("tokens={} lines={}", tokens.len(), src.lines().count());
    Ok(())
}
