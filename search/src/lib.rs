#[macro_use]
extern crate lazy_static;

extern crate serde;
extern crate schemafy;
extern crate serde_json;

use std::io::prelude::*;
use std::fs::File;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use serde::{Serialize, Deserialize};
use std::io::BufReader;
use eddie::JaroWinkler;

schemafy::schemafy!(
    root: Schema
    "src/schema.json"
);

// Source: https://github.com/serde-rs/serde/issues/1195
pub fn read_file(file: zip::read::ZipFile)-> String {
    let mut buffered_reader = BufReader::new(file);
    let mut contents = String::new();
    let _number_of_bytes: usize = match buffered_reader.read_to_string(&mut contents) {
        Ok(number_of_bytes) => number_of_bytes,
        Err(_err) => 0
    };

    contents
}

static N: i32 = 4;
lazy_static! {
    static ref companies: Vec<Schema> = {
        println!("+++ Initialize Datenanfragen... +++");

        let file: File = File::open("src/companies.zip").unwrap();
        let mut zip: zip::ZipArchive<File> = zip::ZipArchive::new(file).unwrap();
 
        let mut array: Vec<Schema> = Vec::with_capacity(zip.len()-1);

        for i in 1..zip.len()
        {
            let f = zip.by_index(i).unwrap();
            let content: String = read_file(f);
            let data: Schema = serde_json::from_str(&content).unwrap();
            array.push(data);
        }
        println!("+++ Initialization of Datenanfragen module completed – {} companies loaded +++", (zip.len()-1).to_string());
        array
    };
}

#[pyfunction]
fn search_company(name: String, count: usize) -> PyResult<Vec<String>> {
    let jarwin = JaroWinkler::new();
    let mut companies_clone = companies.clone();
    companies_clone.sort_by(|b,a| jarwin.similarity(&(name.to_lowercase()), &(a.name.to_lowercase())).partial_cmp(&jarwin.similarity(&(name.to_lowercase()), &(b.name.to_lowercase()))).unwrap());
    let names: Vec<String> = companies_clone.into_iter().take(count).map(|c| c.name).collect();
    Ok(names)
}

#[pymodule]
fn datenanfragen(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(search_company))?;

    Ok(())
}