import { useEffect, useState } from "react";

import api from "../services/api";

import Navbar from "../components/Navbar";

export default function Dashboard() {

    const [tasks, setTasks] = useState([]);

    const [title, setTitle] = useState("");

    const [description, setDescription] = useState("");

    async function loadTasks() {

        const res = await api.get("/tasks/");

        setTasks(res.data.data);

    }

    useEffect(() => {

        loadTasks();

    }, []);

    async function createTask(e) {

        e.preventDefault();

        await api.post("/tasks/", {

            title,

            description

        });

        setTitle("");

        setDescription("");

        loadTasks();

    }

    async function deleteTask(id) {

        await api.delete(`/tasks/${id}`);

        loadTasks();

    }

    async function toggleComplete(task) {

        await api.put(`/tasks/${task._id}`, {

            completed: !task.completed

        });

        loadTasks();

    }

    const totalCount = tasks.length;

    const doneCount = tasks.filter(t => t.completed).length;

    const pendingCount = totalCount - doneCount;

    const donePercent = totalCount === 0 ? 0 : Math.round((doneCount / totalCount) * 100);

    return (

        <>

            <Navbar />

            <div className="dashboard">

                <div className="dashboard-head">

                    <h1>Your tasks</h1>

                    <p>Track what's next and what's already done.</p>

                </div>

                <div className="stats-strip">

                    <div className="stat-card stat-progress">

                        <div className="stat-label">Overall progress</div>

                        <div className="stat-value">{donePercent}<span style={{fontSize:'1rem', color:'var(--text-dim)'}}>%</span></div>

                        <div className="stat-track">

                            <div
                                className="stat-track-fill"
                                style={{ width: `${donePercent}%` }}
                            />

                        </div>

                    </div>

                    <div className="stat-card stat-pending">

                        <div className="stat-label">Pending</div>

                        <div className="stat-value">{pendingCount}</div>

                    </div>

                    <div className="stat-card stat-done">

                        <div className="stat-label">Completed</div>

                        <div className="stat-value">{doneCount}</div>

                    </div>

                </div>

                <form
                    className="task-form"
                    onSubmit={createTask}
                >

                    <h3>Create Task</h3>

                    <input

                        placeholder="Title"

                        value={title}

                        onChange={(e)=>setTitle(e.target.value)}

                    />

                    <textarea

                        placeholder="Description"

                        value={description}

                        onChange={(e)=>setDescription(e.target.value)}

                    />

                    <button className="btn btn-primary">

                        Add Task

                    </button>

                </form>

                <div className="tasks">

                    {

                        tasks.length === 0 &&

                        <div className="empty-state">

                            <div className="empty-glyph">Nothing here yet</div>

                            <p>Add your first task above to get started.</p>

                        </div>

                    }

                    {

                        tasks.map(task=>(

                            <div
                                key={task._id}
                                className={`task-card ${task.completed ? "is-done" : ""}`}
                            >

                                <div className="task-card-top">

                                    <h3>

                                        {task.title}

                                    </h3>

                                    <span className={`status-pill ${task.completed ? "done" : "pending"}`}>

                                        {

                                            task.completed

                                            ?

                                            "Completed"

                                            :

                                            "Pending"

                                        }

                                    </span>

                                </div>

                                <p className="task-desc">

                                    {task.description}

                                </p>

                                <div className="task-card-actions">

                                    <button
                                        className="task-action-btn"
                                        onClick={()=>toggleComplete(task)}
                                    >

                                        Toggle

                                    </button>

                                    <button
                                        className="task-action-btn danger"
                                        onClick={()=>deleteTask(task._id)}
                                    >

                                        Delete

                                    </button>

                                </div>

                            </div>

                        ))

                    }

                </div>

            </div>

        </>

    );

}
