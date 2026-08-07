from vivalab.etl.patient_etl import PatientETL


def main():

    patient_etl = PatientETL()
    patient_etl.run()


if __name__ == "__main__":
    main()