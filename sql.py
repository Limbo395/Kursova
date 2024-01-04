import pymysql
from config import host, user, password, db_name

try:
    conection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Successfully connected...")
    print("#" * 20)



    def show_all(variant):
            with conection.cursor() as cursor:
                match variant:
                    case "BRV":
                        cursor.execute("SELECT * from `BRV`")
                    case "RRV":
                        cursor.execute("SELECT * from `RRV`")
                    case "TRV":
                        cursor.execute("SELECT * from `TRV`")
                    case "DIV":
                        cursor.execute("SELECT * from `SourcesOfIonizingRadiation`")
                    case "Storages":
                        cursor.execute("SELECT * from `Storages`")
                    case "Vocabulare_StorageId":
                        cursor.execute("SELECT ID, NameOfStorage from `Storages`")
                    case "Vocabulare_StorageCondition":
                        cursor.execute("SELECT ID_Of_States, NameOfStates from `DirectoryOfStates`")
                    case "Vocabulare_StorageMethods":
                        cursor.execute("SELECT ID_OfStorageMethod, NameOfStorageMethod, TemperatereRequirementsInStorage, PressureRequirementsInStorage from `DirectoryOfStorageMethods`")
                    case "Vocabulare_TypesOfStorage":
                        cursor.execute("SELECT ID_OfType, NameOfTypes from `DirectoryOfTypes`")
                
                return cursor.fetchall()
    def update_row(variant, values):
        with conection.cursor() as cursor:
            match variant:
                case "BRV":
                    update_query = "UPDATE `BRV` SET ID_Of_BRV = %s, ID_OfStorage = %s, GroupOf_BRV = %s, GeneralActivity = %s, ID_OfRadionuclideDirectory = %s, DateOfReceipt = %s, ManufacturerOrSource = %s, ID_StorageMethod = %s WHERE ID_Of_BRV = %s"
                case "RRV":
                    update_query = "UPDATE `RRV` SET ID_Of_RRV = %s, ID_OfStorage = %s, CategoryOf_RRV = %s, Characteristic = %s, GeneralActivity = %s, ID_OfRadionuclideDirectory = %s, DateOfReceipt = %s, ManufacturerOrSource = %s, ID_StorageMethod = %s WHERE ID_Of_RRV = %s"
                case "TRV":
                    update_query = "UPDATE `TRV` SET ID_Of_TRV = %s, ID_OfStorage = %s, GroupOf_TRV = %s, GeneralActivity = %s, ID_OfRadionuclideDirectory = %s, DateOfReceipt = %s, ManufacturerOrSource = %s, ID_StorageMethod = %s WHERE ID_Of_TRV = %s"
                case "DIV":
                    update_query = "UPDATE `SourcesOfIonizingRadiation` SET ID_SourcesOfIonizingRadiation = %s, ID_OfStorage = %s, ID_OfRadionuclideDirectory = %s, Activity = %s, DateOfManufacture = %s, DateOfReceipt = %s, TermsOfServiceOfSIR = %s, NameOfTheDevice = %s, ManufucturerOrSource = %s, ID_StorageMethod = %s WHERE ID_SourcesOfIonizingRadiation = %s"
                case "Storages":
                    update_query = "UPDATE `Storages` SET NameOfStorage = %s, Location = %s, StorageCondition = %s, TypeOfStorageID = %s, StorageVolume = %s, CertificateID = %s, DateOfVerification = %s,  WHERE ID = %s"
            values.append(values[0]) 
            cursor.execute(update_query, values)
            conection.commit()

    def delete_row_table(variant, row_id):
        with conection.cursor() as cursor:
            match variant:
                case "BRV":
                    delete_query = "DELETE FROM `BRV` WHERE ID_Of_BRV = %s"
                case "RRV":
                    delete_query = "DELETE FROM `RRV` WHERE ID_Of_RRV = %s"
                case "TRV":
                    delete_query = "DELETE FROM `TRV` WHERE ID_Of_TRV = %s"
                case "DIV":
                    delete_query = "DELETE FROM `SourcesOfIonizingRadiation` WHERE ID_SourcesOfIonizingRadiation = %s"
                case "Storages":
                    delete_query = "DELETE FROM `Storages` WHERE ID = %s"
            cursor.execute(delete_query, (row_id,))
            conection.commit()

    def insert_row(variant, values):
        with conection.cursor() as cursor:
            match variant:
                case "BRV":
                    insert_query = "INSERT INTO `BRV` (ID_Of_BRV, ID_OfStorage, GroupOf_BRV, GeneralActivity, ID_OfRadionuclideDirectory, DateOfReceipt, ManufacturerOrSource, Id_StorageMethod) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                case "RRV":
                    insert_query = "INSERT INTO `RRV` (ID_Of_RRV, ID_OfStorage, CategoryOf_RRV, Characteristic, GeneralActivity, ID_OfRadionuclideDirectory, DateOfReceipt, ManufacturerOrSource, Id_StorageMethod) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                case "TRV":
                    insert_query = "INSERT INTO `TRV` (ID_Of_TRV, ID_OfStorage, GroupOf_TRV, GeneralActivity, ID_OfRadionuclideDirectory, DateOfReceipt, ManufacturerOrSource, Id_StorageMethod) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                case "DIV":
                    insert_query = "INSERT INTO `SourcesOfIonizingRadiation` (ID_SourcesOfIonizingRadiation, ID_OfStorage, ID_OfRadionuclideDirectory, Activity, DateOfManufacture, DateOfReceipt, TermsOfServiceOfSIR, Name Of The Device, ManufuctureOrSource, Id_StorageMethod) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                case "Storages":
                    insert_query = "INSERT INTO `Storages` (ID, NameOfStorage, Location, StorageCondition, TypeOfStorageID, StorageVolume, CertificateID, DateOfVerification) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, values)
            conection.commit()












except Exception as ex:
    print("Conection refused...")
    print(ex)
    exit(0)