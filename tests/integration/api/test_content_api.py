from uuid import uuid4

import pytest

@pytest.mark.asyncio
async def test_get_courses_returns_public_list(client, seeded_course_tree):
    response = await client.get('/api/courses')

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]['title'] == seeded_course_tree.course_title

@pytest.mark.asyncio
async def test_get_course_returns_single_course(client, seeded_course_tree):
    response = await client.get(f'/api/courses/{seeded_course_tree.course_id}')

    assert response.status_code == 200
    payload = response.json()
    assert payload['id'] == seeded_course_tree.course_id
    assert payload['title'] == seeded_course_tree.course_title

@pytest.mark.asyncio
async def test_get_course_returns_404_when_course_is_missing(client):
    response = await client.get(f'/api/courses/{uuid4()}')

    assert response.status_code == 404
    payload = response.json()
    assert payload['error'] == 'course_not_found'

@pytest.mark.asyncio
async def test_get_course_structure_returns_modules_sections_and_lectures(client, seeded_course_tree):
    response = await client.get(f'/api/courses/{seeded_course_tree.course_id}/structure')

    assert response.status_code == 200
    payload = response.json()
    assert payload['title'] == seeded_course_tree.course_title
    assert len(payload['modules']) == 1
    assert len(payload['modules'][0]['sections']) == 1
    assert len(payload['modules'][0]['sections'][0]['lectures']) == 1

@pytest.mark.asyncio
async def test_get_lecture_returns_full_content(client, seeded_course_tree):
    response = await client.get(f'/api/lectures/{seeded_course_tree.lecture_id}')

    assert response.status_code == 200
    payload = response.json()
    assert payload['id'] == seeded_course_tree.lecture_id
    assert payload['content'] == seeded_course_tree.lecture_content