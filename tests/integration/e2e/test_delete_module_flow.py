import pytest


@pytest.mark.asyncio
async def test_delete_module_updates_public_structure_and_hides_subtree(
    client,
    admin_auth_headers,
):
    headers = admin_auth_headers

    course_response = await client.post(
        '/api/admin/courses',
        headers=headers,
        json={
            'title': 'FastAPI course',
            'description': 'Clean architecture in practice.',
        },
    )
    assert course_response.status_code == 201
    course_id = course_response.json()['id']

    kept_module_response = await client.post(
        f'/api/admin/courses/{course_id}/modules',
        headers=headers,
        json={
            'title': 'Kept module',
            'description': 'Should remain after delete.',
            'position': 1,
        },
    )
    assert kept_module_response.status_code == 201
    kept_module_id = kept_module_response.json()['id']

    kept_section_response = await client.post(
        f'/api/admin/modules/{kept_module_id}/sections',
        headers=headers,
        json={
            'title': 'Kept section',
            'description': 'Should remain after delete.',
            'position': 1,
        },
    )
    assert kept_section_response.status_code == 201
    kept_section_id = kept_section_response.json()['id']

    kept_lecture_response = await client.post(
        f'/api/admin/sections/{kept_section_id}/lectures',
        headers=headers,
        json={
            'title': 'Kept lecture',
            'content': 'Kept lecture content',
            'position': 1,
        },
    )
    assert kept_lecture_response.status_code == 201
    kept_lecture_id = kept_lecture_response.json()['id']

    deleted_module_response = await client.post(
        f'/api/admin/courses/{course_id}/modules',
        headers=headers,
        json={
            'title': 'Deleted module',
            'description': 'Will be removed with subtree.',
            'position': 2,
        },
    )
    assert deleted_module_response.status_code == 201
    deleted_module_id = deleted_module_response.json()['id']

    deleted_section_response = await client.post(
        f'/api/admin/modules/{deleted_module_id}/sections',
        headers=headers,
        json={
            'title': 'Deleted section',
            'description': 'Should disappear with module.',
            'position': 1,
        },
    )
    assert deleted_section_response.status_code == 201
    deleted_section_id = deleted_section_response.json()['id']

    deleted_lecture_response = await client.post(
        f'/api/admin/sections/{deleted_section_id}/lectures',
        headers=headers,
        json={
            'title': 'Deleted lecture',
            'content': 'Deleted lecture content',
            'position': 1,
        },
    )
    assert deleted_lecture_response.status_code == 201
    deleted_lecture_id = deleted_lecture_response.json()['id']

    structure_before = await client.get(f'/api/courses/{course_id}/structure')
    assert structure_before.status_code == 200
    assert len(structure_before.json()['modules']) == 2

    delete_response = await client.delete(
        f'/api/admin/modules/{deleted_module_id}',
        headers=headers,
    )
    assert delete_response.status_code == 204

    course_response_after = await client.get(f'/api/courses/{course_id}')
    assert course_response_after.status_code == 200

    structure_after = await client.get(f'/api/courses/{course_id}/structure')
    assert structure_after.status_code == 200
    structure_payload = structure_after.json()
    assert len(structure_payload['modules']) == 1
    remaining_module = structure_payload['modules'][0]
    assert remaining_module['id'] == kept_module_id
    assert len(remaining_module['sections']) == 1
    assert remaining_module['sections'][0]['id'] == kept_section_id
    assert len(remaining_module['sections'][0]['lectures']) == 1
    assert remaining_module['sections'][0]['lectures'][0]['id'] == kept_lecture_id

    module_ids_in_structure = {module['id'] for module in structure_payload['modules']}
    assert deleted_module_id not in module_ids_in_structure
    section_ids_in_structure = {
        section['id']
        for module in structure_payload['modules']
        for section in module['sections']
    }
    assert deleted_section_id not in section_ids_in_structure

    deleted_lecture_read = await client.get(f'/api/lectures/{deleted_lecture_id}')
    assert deleted_lecture_read.status_code == 404

    kept_lecture_read = await client.get(f'/api/lectures/{kept_lecture_id}')
    assert kept_lecture_read.status_code == 200
    assert kept_lecture_read.json()['content'] == 'Kept lecture content'
