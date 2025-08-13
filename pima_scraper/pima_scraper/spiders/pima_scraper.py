import scrapy

class CaseSpider(scrapy.Spider):
    name = "case_spider"

    def __init__(self, start_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if start_id is None:
            raise ValueError("You must provide a start_id")
        self.current_id = int(start_id)

    def start_requests(self):
        # Start scraping from the initial ID
        yield scrapy.Request(
            url=f"https://www.cosc.pima.gov/PublicDocs/GetCase2.aspx?ID={self.current_id}",
            callback=self.parse
        )

    def parse(self, response):
        # Check if case_number exists; if not, stop spider
        case_number = response.css("#txtCaseNumber::attr(value)").get()
        if not case_number:
            self.logger.info(f"No data found for ID {self.current_id}. Stopping spider.")
            return  # Stop scraping

        filing_date = response.css("#txtCaseDate::attr(value)").get()
        caption = response.css("#txtCaseCaption::text").get()
        judge = response.css("#txtJudge::attr(value)").get()

        # Extract parties
        parties = []
        for row in response.css("#grdParty tr")[1:]:
            party_full_name = row.css("td:nth-child(1) *::text").get()
            party_role = row.css("td:nth-child(2) *::text").get()
            name_type = row.css("td:nth-child(3) *::text").get()
            dob = row.css("td:nth-child(4) *::text").get()
            if party_full_name or party_role or name_type or dob:
                parties.append({
                    "party_full_name": party_full_name.strip() if party_full_name else None,
                    "party_role": party_role.strip() if party_role else None,
                    "name_type": name_type.strip() if name_type else None,
                    "dob": dob.strip() if dob else None
                })

        yield {
            "case_number": case_number.strip(),
            "filing_date": filing_date.strip() if filing_date else None,
            "caption": caption.strip() if caption else None,
            "judge": judge.strip() if judge else None,
            "parties": parties
        }

        # Increment ID and request next page
        self.current_id += 1
        next_url = f"https://www.cosc.pima.gov/PublicDocs/GetCase2.aspx?ID={self.current_id}"
        yield scrapy.Request(url=next_url, callback=self.parse)