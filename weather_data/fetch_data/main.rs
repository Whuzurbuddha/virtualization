use std::error::Error;
use chrono::prelude::*;
use mysql::Pool;
use mysql::prelude::Queryable;
use reqwest;
use scraper::{Html, Selector};

fn insert_into_database(value: f64, date: NaiveDate, db_type: &str) -> Result<(), Box<dyn Error>>{
    let username = user;
    let pwd = pwd;
    let host = "127.0.0.1";
    let port = "3306";
    let db = "weatherdata";
    let url = format!(
        "mysql://{}:{}@{}:{}/{}",
        username,
        pwd,
        host,
        port,
        db
    );
    let pool = Pool::new(&*url)?;
    let mut conn = pool.get_conn()?;

    let sql;

    match db_type{
        "temp" => {
            sql = r"INSERT INTO temperatures (date, temp) VALUES (?, ?)";
            conn.exec_drop(sql, (date.to_string(), value))?;
        },
        "preci" => {
            sql = r"INSERT INTO precipitation (date, value) VALUES (?, ?)";
            conn.exec_drop(sql, (date.to_string(), value))?;
        },
        _=> eprintln!("Error while inserting data into database")
    }

    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let response = reqwest::get(
        "https://www.wetter.com/deutschland/rostock/gross-klein/DE2915417.html"
    )
        .await?
        .text()
        .await?;

    let document = Html::parse_document(&response);
    let temp_selector = Selector::parse(
        ".weather-overview > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > span:nth-child(1)"
    )
        .unwrap();
    let preci_selector = Selector::parse(
        ".weather-overview > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(3)"
    )
        .unwrap();

    let today = Utc::now().date_naive();

    let temp = document.select(&temp_selector).map(|x| x.inner_html());
    let preci = document.select(&preci_selector).map(|x| x.inner_html());
    for (item, _number) in temp.zip(1..2) {
        let temp_value = item.replace("°", "").parse::<f64>()?;
        if let Err(e) = insert_into_database(temp_value, today, "temp") {
            eprintln!("Fehler beim Einfügen in die Datenbank: {}", e);
        }
    }
    for (item, _number) in preci.zip(1..2) {
        let cleaned_input: String = item.chars()
            .filter(|&c| c.is_digit(10) || c == ',' || c == '.')
            .collect();
        if let Ok(value) = cleaned_input.replace(",", ".")
            .parse::<f64>(){
            if let Err(e) = insert_into_database(value, today, "preci") {
                eprintln!("Fehler beim Einfügen in die Datenbank: {}", e);
            }
        }
    }

    Ok(())
}
