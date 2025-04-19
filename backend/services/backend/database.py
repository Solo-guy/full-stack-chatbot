from ...utils.db import get_cockroach_session, get_scylla_session, get_postgres_session

def manage_database(action: str, params: dict) -> dict:
    """
    Manage database operations (query, optimize).
    """
    try:
        if action == "query_cockroach":
            # Thực thi truy vấn CockroachDB
            with get_cockroach_session() as session:
                result = session.execute(params.get("query")).fetchall()
                return {"result": [dict(row) for row in result]}

        elif action == "query_scylla":
            # Thực thi truy vấn ScyllaDB
            with get_scylla_session() as session:
                result = session.execute(params.get("query")).all()
                return {"result": [dict(row) for row in result]}

        elif action == "query_postgres":
            # Thực thi truy vấn PostgreSQL
            with get_postgres_session() as session:
                result = session.execute(params.get("query")).fetchall()
                return {"result": [dict(row) for row in result]}

        elif action == "optimize":
            # Tối ưu hóa index (giả lập)
            with get_cockroach_session() as session:
                session.execute(f"CREATE INDEX IF NOT EXISTS idx_{params.get('table')}_{params.get('column')} ON {params.get('table')} ({params.get('column')})")
                session.commit()
            return {"message": f"Index created on {params.get('table')}.{params.get('column')}"}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}