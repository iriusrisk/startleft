from unittest.mock import MagicMock

from startleft.project.otm_project import OtmProject
from startleft.project.otm_project_service import OtmProjectService
from tests.resources import test_resource_paths

iriusrisk_project_repository = MagicMock()
otm_project_service = OtmProjectService(iriusrisk_project_repository)


class TestOtmProjectService:

    def test_create_project_otm_file_ok(self):
        # Given a valid OTM project
        otm_project = OtmProject.from_otm_file(test_resource_paths.otm_file_example, 'id', 'name')

        # When calling create_project
        otm_project_service.create_project(otm_project)

        # Then
        assert iriusrisk_project_repository.create.called

    def test_update_project_otm_file_ok(self):
        # Given a valid existing OTM project
        otm_project = OtmProject.from_otm_file(test_resource_paths.otm_file_example, 'existing-project-id',
                                               'existing-project-name')

        # When calling update_project
        otm_project_service.update_project(otm_project)

        # Then
        assert iriusrisk_project_repository.update.called

    def test_recreate_non_existing_project_otm_file_ok(self):
        # Given a valid non existing OTM project
        otm_project = OtmProject.from_otm_file(test_resource_paths.otm_file_example, 'non-existing-project-id',
                                               'non-existing-project-id')

        # And a mocked non-existing project response
        iriusrisk_project_repository.exists.return_value = False

        # When calling recreate_project
        otm_project_service.recreate_project(otm_project)

        # Then
        assert not iriusrisk_project_repository.delete.called
        assert iriusrisk_project_repository.create.called

    def test_recreate_existing_project_otm_file_ok(self):
        # Given a valid non existing OTM project
        otm_project = OtmProject.from_otm_file(test_resource_paths.otm_file_example, 'existing-project-id',
                                               'existing-project-id')

        # And a mocked non-existing project response
        iriusrisk_project_repository.exists.return_value = True

        # When calling recreate_project
        otm_project_service.recreate_project(otm_project)

        # Then
        assert iriusrisk_project_repository.delete.called
        assert iriusrisk_project_repository.create.called

    def test_update_or_create_non_existing_project_otm_file_ok(self):
        # Given a valid non existing OTM project
        otm_project = OtmProject.from_otm_file(test_resource_paths.otm_file_example, 'non-existing-project-id',
                                               'non-existing-project-id')

        # And a mocked non-existing project response
        iriusrisk_project_repository.exists.return_value = False

        # When calling update_or_create_project
        otm_project_service.update_or_create_project(otm_project)

        # Then
        assert iriusrisk_project_repository.create.called

    def test_update_or_create_existing_project_otm_file_ok(self):
        # Given a valid non existing OTM project
        otm_project = OtmProject.from_otm_file(test_resource_paths.otm_file_example, 'existing-project-id',
                                               'existing-project-id')

        # And a mocked non-existing project response
        iriusrisk_project_repository.exists.return_value = True

        # When calling update_or_create_project
        otm_project_service.recreate_project(otm_project)

        # Then
        assert iriusrisk_project_repository.update.called
