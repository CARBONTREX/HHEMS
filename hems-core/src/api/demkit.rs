use std::{num::ParseFloatError, str::FromStr, sync::OnceLock};

use num_complex::{Complex, ParseComplexError};
use once_cell::sync::Lazy;
use reqwest;
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;


pub mod battery;
pub mod meter;
pub mod solar;
pub mod thermal;
pub mod timeshifters;
pub mod devices;
pub mod ha_entity;
pub mod env;
pub mod sim;

static BASE_URL: Lazy<String> = Lazy::new(|| {
    std::env::var("DEMKIT_URL").expect("DEMKIT_URL is not set")
});

static CLIENT: OnceLock<reqwest::Client> = OnceLock::new();

pub fn init() -> reqwest::Client {
    reqwest::Client::new()
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct Measurement {
    pub value: f64,
    pub unit: String,
}

#[derive(Deserialize, Debug, Clone)]
#[serde(untagged)]
pub enum Commodity {
    #[serde(rename = "complex")]
    Complex(String),
    #[serde(rename = "real")]
    Real(f64),
}

#[derive(Deserialize, Debug)]
pub struct Commodities {
    #[serde(rename = "ELECTRICITY")]
    pub electricity: Option<Commodity>,
    #[serde(rename = "HEAT")]
    pub heat: Option<Commodity>,
}

#[derive(thiserror::Error, Debug)]
pub enum ApiError {
    #[error("Request failed: {0}")]
    ReqwestError(#[from] reqwest::Error),
    #[error("Serde error: {0}")]
    SerdeError(#[from] serde_json::Error),
    #[error("Parse error: {0}")]
    ParseError(#[from] ParseComplexError<ParseFloatError>),
    #[error("DEMKIT API error: {0}")]
    DemkitError(String),
}

fn parse_complex_str(
    input: &Commodity,
) -> Result<Complex<f64>, ParseComplexError<ParseFloatError>> {
    match input {
        Commodity::Complex(input) => {
            Complex::from_str(&input[2..].replace("(", "").replace(")", ""))
        }
        Commodity::Real(input) => Ok(Complex::new(*input, 0.0)),
    }
}


pub async fn get_time() -> u64 {
    let client = CLIENT.get_or_init(init);

    let url = format!("{}/time", *BASE_URL);

    let response = client.get(url).send().await.unwrap();

    response.json::<u64>().await.unwrap()
}


pub async fn list_entities() -> Vec<String> {
    let client = CLIENT.get_or_init(init);

    let url = format!("{}/list", *BASE_URL);

    let response = client.get(url).send().await.unwrap();

    let response_body = response.json::<Vec<String>>().await.unwrap();

    response_body
}