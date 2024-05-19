
<a name="readme-top"></a>
<h3 align="center">Fixr Bot</h3>

<p align="center">
  Automated Ticket Purchasing Bot
  <br />
</p>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#motivation">Motivation</a></li>
        <li><a href="#features">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#details">Details</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

The Fixr Bot is a project designed to automate the process of creating accounts and purchasing tickets on the Fixr platform. The bot uses a Selenium Python script for account creation and a Go package API to purchase tickets using those accounts.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Motivation

This project was inspired by the need to automate repetitive tasks associated with ticket purchasing, reducing the time and effort required for manual account creation and ticket booking.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Features

- Automated account creation using Selenium.
- Ticket purchasing via a Go package API.
- Error handling and logging for robust operation.
- Customizable for different ticket purchasing scenarios.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* ![Python][Python-img]
* ![Selenium][Selenium-img]
* ![Go][Go-img]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Before you begin, ensure you have the following prerequisites installed:

- [Python](https://www.python.org/)
- [Go](https://golang.org/)
- [Selenium WebDriver](https://www.selenium.dev/documentation/en/webdriver/)
- [Google Chrome](https://www.google.com/chrome/) or [Chromium](https://www.chromium.org/)

### Installation

Follow these steps to install and set up the project:

1. Clone the repository: 

    ```bash
    git clone https://github.com/sneakypanda17/fixr_bot.git
    ```

2. Navigate to the project directory: 

    ```bash
    cd fixr_bot
    ```

3. Set up a virtual environment for Python:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

4. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

5. Install the Go dependencies:

    ```bash
    go mod tidy
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

To run the bot, follow these steps:

1. Activate the Python virtual environment:

    ```bash
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

2. Run the Python script for account creation:

    ```bash
    python account_creation.py
    ```

3. Use the Go package to purchase tickets:

    ```bash
    go run main.go
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PROJECT STRUCTURE -->
## Project Structure

Here is an overview of the project's structure:

```plaintext
fixr_bot/
├── account_creation/
│   ├── account_creation.py
│   ├── unused_accounts.csv
├── credential_generator/
│   ├── raw_data/
│   │   ├── firstnames.csv
│   │   ├── surnames.csv
│   │   ├── words.csv
│   ├── credential_generator.py
│   ├── credentials_record.csv
│   ├── credentials.csv
├── main/
│   ├── main.exe
│   ├── main.go
├── web_scraper/
│   ├── events.json
│   ├── web_scraper.py
├── .gitignore
├── LICENSE.txt
├── README.md
├── requirements.txt
```

- **account_creation/**: Contains the Python script and output CSV for account creation.
- **credential_generator/**: Contains the scripts and data for generating credentials.
- **main/**: Contains the Go script for ticket purchasing.
- **web_scraper/**: Contains the script and data for web scraping.
- **.gitignore**: Specifies files and directories to be ignored by git.
- **LICENSE.txt**: The license for the project.
- **README.md**: This README file.
- **requirements.txt**: Lists Python dependencies.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repository and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DETAILS -->
## Details

- **Author:** Sneaky Panda
- **Source code:** [GitHub Repository](https://github.com/sneakypanda17/fixr_bot)
- **Acknowledgments:** This project was inspired by the need for automating repetitive tasks related to ticket purchasing.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

- [Selenium](https://www.selenium.dev/)
- [Go](https://golang.org/)
- [Python](https://www.python.org/)
- [GitHub](https://github.com/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Python-img]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Selenium-img]: https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white
[Go-img]: https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white
