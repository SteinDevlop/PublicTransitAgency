class Reports ():

    def __init__(self, type: str, id_report: int, generated_data: str):
        self.type = type
        self.id_report = id_report
        self.generated_data = generated_data
    
    def generate_report(self):
        if not self.type or not self.generated_data:
            raise ValueError("Type and generated data are required.")
        
        print(f"Generating report: {self.type}, Data: {self.generated_data}")
        return True
    
    def export (self):
        if not self.id_report:
            raise ValueError("Report ID is required.")
        print(f"Exporting report ID {self.id_report}")
        return True
    