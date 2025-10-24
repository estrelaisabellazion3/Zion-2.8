use nom::{
    branch::alt,
    bytes::complete::{tag, take_while, take_while1},
    character::complete::{char, digit1, multispace0, multispace1},
    combinator::{map, opt, recognize},
    multi::many0,
    sequence::{delimited, preceded, tuple},
    IResult,
};
use anyhow::Result;

use crate::ast::{Algorithm, Ast, Function, FunctionKind, QuantumDecl, Span, ToneDecl};

pub fn build_ast(src: &str) -> Result<Ast> {
    println!("DEBUG: Parsing source:\n{}", src);
    match parse_zqal(src) {
        Ok((_, ast)) => {
            println!("DEBUG: Parse successful");
            Ok(ast)
        },
        Err(e) => {
            println!("DEBUG: Parse error: {:?}", e);
            Err(anyhow::anyhow!("Parse error: {:?}", e))
        },
    }
}

fn parse_zqal(input: &str) -> IResult<&str, Ast> {
    let (input, _) = multispace0(input)?;

    // Parse all declarations in any order using a simple loop
    let mut algorithm: Option<Algorithm> = None;
    let mut functions: Vec<Function> = Vec::new();
    let mut quantum: Vec<QuantumDecl> = Vec::new();
    let mut tones: Vec<ToneDecl> = Vec::new();

    let mut remaining = input;
    // Try to parse functions only for now
    while !remaining.trim().is_empty() {
        match parse_function(remaining) {
            Ok((rest, func)) => {
                remaining = rest;
                functions.push(func);
                remaining = multispace0(remaining)?.0;
            }
            Err(_) => {
                // Skip this line
                if let Some(newline_pos) = remaining.find('\n') {
                    remaining = &remaining[newline_pos + 1..];
                } else {
                    break;
                }
            }
        }
    }

    Ok((remaining, Ast {
        algorithm,
        functions,
        quantum,
        tones,
    }))
}

#[derive(Debug)]
enum Declaration {
    Algorithm(Algorithm),
    Function(Function),
    Quantum(QuantumDecl),
    Tone(ToneDecl),
    Import,
    Const,
}

fn parse_algorithm(input: &str) -> IResult<&str, Algorithm> {
    let (input, _) = multispace0(input)?; // Skip leading whitespace
    let (input, _) = tag("@algorithm")(input)?;
    let (input, _) = multispace1(input)?;
    let (input, name) = parse_identifier(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = char('{')(input)?;
    // Skip algorithm body - can contain version, target, etc.
    let (input, _) = skip_block(input)?;

    let span = Span { start: 0, end: 0 }; // TODO: proper span calculation
    Ok((input, Algorithm { name: name.to_string(), span }))
}

fn parse_function(input: &str) -> IResult<&str, Function> {
    println!("DEBUG: parse_function called with: {:?}", &input[..50]);
    let (input, _) = multispace0(input)?; // Skip leading whitespace
    println!("DEBUG: after multispace0: {:?}", &input[..50]);
    let (input, kind) = alt((
        map(tag("@kernel"), |_| FunctionKind::Kernel),
        map(tag("@validator"), |_| FunctionKind::Validator),
        map(tag("@reward"), |_| FunctionKind::Reward),
    ))(input)?;
    println!("DEBUG: parsed kind: {:?}", kind);
    let (input, _) = multispace1(input)?;
    let (input, _) = tag("fn")(input)?;
    let (input, _) = multispace1(input)?;
    let (input, name) = parse_identifier(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = char('(')(input)?;
    // Skip parameters for now
    let (input, _) = take_while(|c| c != ')')(input)?;
    let (input, _) = char(')')(input)?;
    let (input, _) = multispace0(input)?;
    let (input, return_type) = opt(parse_return_type)(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = char('{')(input)?;
    // Skip function body
    let (input, _) = skip_block(input)?;

    let span = Span { start: 0, end: 0 }; // TODO: proper span calculation
    Ok((input, Function {
        kind,
        name: name.to_string(),
        return_type: return_type.map(|s| s.to_string()),
        span,
    }))
}

fn parse_return_type(input: &str) -> IResult<&str, &str> {
    let (input, _) = tag("->")(input)?;
    let (input, _) = multispace0(input)?;
    parse_type(input)
}

fn parse_quantum_decl(input: &str) -> IResult<&str, QuantumDecl> {
    let (input, _) = multispace0(input)?; // Skip leading whitespace
    let (input, _) = tag("quantum")(input)?;
    let (input, _) = multispace1(input)?;
    let (input, name) = parse_identifier(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = char('[')(input)?;
    let (input, size_str) = digit1(input)?;
    let (input, _) = char(']')(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = char(':')(input)?;
    let (input, _) = multispace0(input)?;
    let (input, ty) = parse_type(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = char(';')(input)?;

    let size: u32 = size_str.parse().unwrap_or(0);
    let span = Span { start: 0, end: 0 }; // TODO: proper span calculation
    Ok((input, QuantumDecl {
        name: name.to_string(),
        size,
        ty: ty.to_string(),
        span,
    }))
}

fn parse_tone_decl(input: &str) -> IResult<&str, ToneDecl> {
    let (input, _) = multispace0(input)?; // Skip leading whitespace
    let (input, _) = tag("@tone")(input)?;
    let (input, _) = multispace1(input)?;
    let (input, id_str) = digit1(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = char('{')(input)?;
    // Skip tone body
    let (input, _) = skip_block(input)?;

    let id: u32 = id_str.parse().unwrap_or(0);
    let span = Span { start: 0, end: 0 }; // TODO: proper span calculation
    Ok((input, ToneDecl { id, span }))
}

fn parse_identifier(input: &str) -> IResult<&str, &str> {
    recognize(tuple((
        take_while1(|c: char| c.is_alphabetic() || c == '_'),
        take_while(|c: char| c.is_alphanumeric() || c == '_'),
    )))(input)
}

fn skip_block(input: &str) -> IResult<&str, ()> {
    let mut depth = 1;
    let mut chars = input.char_indices().peekable();
    let mut end_pos = 0;

    while let Some((pos, ch)) = chars.next() {
        match ch {
            '{' => depth += 1,
            '}' => {
                depth -= 1;
                if depth == 0 {
                    end_pos = pos + 1;
                    break;
                }
            }
            _ => {}
        }
    }

    if depth == 0 {
        Ok((&input[end_pos..], ()))
    } else {
        Err(nom::Err::Error(nom::error::Error::new(input, nom::error::ErrorKind::Char)))
    }
}

fn parse_const(input: &str) -> IResult<&str, ()> {
    let (input, _) = multispace0(input)?; // Skip leading whitespace
    let (input, _) = tag("const")(input)?;
    let (input, _) = multispace1(input)?;
    let (input, _) = parse_identifier(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = char(':')(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = parse_type(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = char('=')(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = take_while(|c| c != ';')(input)?;
    let (input, _) = char(';')(input)?;
    Ok((input, ()))
}

fn parse_import(input: &str) -> IResult<&str, ()> {
    let (input, _) = multispace0(input)?; // Skip leading whitespace
    let (input, _) = alt((tag("import"), tag("from")))(input)?;
    let (input, _) = multispace1(input)?;
    let (input, _) = char('"')(input)?;
    let (input, _) = take_while(|c| c != '"')(input)?;
    let (input, _) = char('"')(input)?;
    let (input, _) = multispace0(input)?;
    let (input, _) = opt(tag("import"))(input)?;
    let (input, _) = multispace0(input)?;
    if let Ok((input, _)) = tag::<_, _, nom::error::Error<_>>("import")(input) {
        let (input, _) = multispace1(input)?;
        let (input, _) = take_while(|c| c != ';')(input)?;
    }
    let (input, _) = char(';')(input)?;
    Ok((input, ()))
}

fn parse_type(input: &str) -> IResult<&str, &str> {
    alt((
        tag("u32"),
        tag("u64"),
        tag("f64"),
        tag("bool"),
        tag("hash32"),
        tag("bytes80"),
        // Reference type like &mut [u32; 12]
        recognize(tuple((
            char('&'),
            opt(tag("mut")),
            multispace0,
            parse_type,
        ))),
        // Array type like [u32; 12]
        recognize(tuple((
            char('['),
            parse_type,
            char(';'),
            digit1,
            char(']'),
        ))),
        parse_identifier,
    ))(input)
}
