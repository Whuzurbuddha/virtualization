use std::error::Error;
use chrono::prelude::*;
use mysql::Pool;
use mysql::prelude::Queryable;
use reqwest;
use scraper::{Html, Selector};

fn insert_into_database(temp: i32, date: NaiveDate) -> Result<(), Box<dyn Error>>{
    let username = username;
    let pwd = password;
    let host = "127.0.0.1";
    let port = "3306";
    let db = database;
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
    let sql = r"INSERT INTO temperatures (date, temp) VALUES (?, ?)";

    conn.exec_drop(sql, (date.to_string(), temp))?;
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
    let today = Utc::now().date_naive();

    let temp = document.select(&temp_selector).map(|x| x.inner_html());
    for (item, _number) in temp.zip(1..2) {
        let temp_value = item.replace("°", "").parse::<i32>()?;
        if let Err(e) = insert_into_database(temp_value, today) {
            eprintln!("Fehler beim Einfügen in die Datenbank: {}", e);
        }
    }

    Ok(())
}
