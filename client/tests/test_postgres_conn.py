import pytest
from unittest.mock import patch, MagicMock
from client.postgres import DatabaseSDKFacade
from models.user_info import EmployeeInfo
from models.message import CustomMessage, HealthMessage


@pytest.fixture
def sample_employee():
    return {
        "id": "1",
        "name": "John Doe",
        "status": "Present",
        "date": "2023-01-01",
    }


@pytest.fixture
def sample_employee_list():
    return [
        {"id": "1", "name": "John Doe", "status": "Present", "date": "2023-01-01"},
        {"id": "2", "name": "Jane Smith", "status": "Absent", "date": "2023-01-02"},
    ]


def test_read_employee_attendance(sample_employee):
    with patch.object(
        DatabaseSDKFacade.database, "read_employee_attendance", return_value=sample_employee
    ):
        result = DatabaseSDKFacade.database.read_employee_attendance(1)
        assert result == sample_employee
        employee_obj = EmployeeInfo(**result)
        assert employee_obj.name == "John Doe"


def test_read_all_employee_attendance(sample_employee_list):
    with patch.object(
        DatabaseSDKFacade.database, "read_all_employee_attendance", return_value=sample_employee_list
    ):
        result = DatabaseSDKFacade.database.read_all_employee_attendance()
        assert result == sample_employee_list
        employee_objs = [EmployeeInfo(**emp) for emp in result]
        assert employee_objs[1].name == "Jane Smith"


def test_create_employee_attendance():
    with patch.object(
        DatabaseSDKFacade.database, "create_employee_attendance", return_value=CustomMessage(
            message="Successfully created the record for the employee id: $1"
        )
    ):
        result = DatabaseSDKFacade.database.create_employee_attendance(
            {"name": "John Doe", "status": "Present", "date": "2023-01-01"}
        )
        assert result.message == "Successfully created the record for the employee id: $1"


def test_attendance_health_up():
    with patch.object(
        DatabaseSDKFacade.database, "attendance_health", return_value=(
            HealthMessage(
                message="Attendance API is running fine and ready to serve requests",
                postgresql="up",
                redis="up",
                status="up",
            ),
            200
        )
    ):
        result, status_code = DatabaseSDKFacade.database.attendance_health()
        assert status_code == 200
        assert result.postgresql == "up"
        assert result.redis == "up"
        assert result.status == "up"
