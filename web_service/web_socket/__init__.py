"""
This spawns a separate thread that listens for a Postgres notification. The
purpose of this module is to create SocketIO notifications, so that a browser
viewing page with study-data can update when new data is posted.
"""
