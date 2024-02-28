# CzaroCRM

CzaroCRM is a web-based application designed to streamline and manage various tasks related to patient care within a hospital setting. The project is developed with Django, a high-level Python web framework.

## User Registration

1. Visit the registration page.
2. Create an account by providing the necessary information.
3. Choose your profession from the available options:
    - Physician
    - Nurse
    - Admin
    - Secretary

## User Roles and Functionalities

### Medical Professionals (Physicians and Nurses)

- **Create and Update Patient Records:**
  - Medical professionals can manage patient information, ensuring accuracy and up-to-date records.

- **Admit Patients to Departments:**
  - Admit patients to specific departments within the hospital.

- **Manage Patient Hospitalization:**
  - Record observations and consultations during a patient's hospitalization.
  - Create and manage various scales such as Norton scales, BMI, NEWS scale, and pain scale.
  - Save patient vital signs to monitor their health status.

- **Transfer and Discharge Patients:**
  - Transfer patients between different hospital departments.
  - Discharge patients when necessary.

### Admins

- **Access to All Features:**
  - Admins have unrestricted access to all features within the application.

- **Manage Departments:**
  - Create, update, and delete hospital departments.

- **Manage Patients:**
  - Create, update, and delete patient records.

### Secretary

- **Manage Patient Records:**
  - Handle patient creation, updates, admissions, and discharges.

- **Transfer and Discharge Patients:**
  - Transfer patients between different hospital departments.
  - Discharge patients as needed.

- **View Patient Data:**
  - Access all patient data, including hospitalization details, observations, and scales.

## Installation

1. Clone the repository:

2. Install dependencies: pip install -r requirements.txt

3. Apply database migrations: python manage.py makemigrations & migrate

4. Run the development server: python manage.py runserver

5. Access the application at [http://localhost:8000/](http://localhost:8000/)

## Usage

1. Create an account and log in.

2. Navigate to different sections based on your role to perform the respective tasks.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.

---

MIT License

Copyright (c) 2024 Mr.Czaro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.