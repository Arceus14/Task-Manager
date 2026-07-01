import { useEffect, useState } from "react";

import api from "../services/api";

import Navbar from "../components/Navbar";

import { isAdmin, getCurrentUserId } from "../utils/auth";

export default function Dashboard() {

    const admin = isAdmin();

    const currentUserId = getCurrentUserId();

    const [tasks, setTasks] = useState([]);

    const [title, setTitle] = useState("");

    const [description, setDescription] = useState("");

    const [feedback, setFeedback] = useState(null);

    function showFeedback(type, message) {

        setFeedback({ type, message });

    }

    useEffect(() => {

        if (!feedback) return;

        const timer = setTimeout(() => setFeedback(null), 4000);

        return () => clearTimeout(timer);

    }, [feedback]);

    function getErrorMessage(err) {

        return err.response?.data?.message || "Something went wrong. Please try again.";

    }

    async function loadTasks() {

        try {

            const res = await api.get("/tasks/");

            setTasks(res.data.data);

        }

        catch (err) {

            showFeedback("error", getErrorMessage(err));

        }

    }

    useEffect(() => {

        loadTasks();

    }, []);

    async function createTask(e) {

        e.preventDefault();

        try {

            await api.post("/tasks/", {

                title,

                description

            });

            setTitle("");

            setDescription("");

            showFeedback("success", "Task added.");

            loadTasks();

        }

        catch (err) {

            showFeedback("error", getErrorMessage(err));

        }

    }

    async function deleteTask(id) {

        try {

            await api.delete(`/tasks/${id}`);

            showFeedback("success", "Task deleted.");

            loadTasks();

        }

        catch (err) {

            showFeedback("error", getErrorMessage(err));

        }

    }

    async function toggleComplete(task) {

        try {

            await api.put(`/tasks/${task._id}`, {

                completed: !task.completed

            });

            showFeedback("success", "Task updated.");

            loadTasks();

        }

        catch (err) {

            showFeedback("error", getErrorMessage(err));

        }

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

                    <div className="dashboard-head-row">

                        <h1>{admin ? "All tasks" : "Your tasks"}</h1>

                        {admin &&

                            <span className="admin-pill">Admin view</span>

                        }

                    </div>

                    <p>

                        {

                            admin

                            ?

                            "Showing tasks from every user."

                            :

                            "Track what's next and what's already done."

                        }

                    </p>

                </div>

                {feedback &&

                    <div className={`feedback-banner ${feedback.type}`}>

                        {feedback.message}

                    </div>

                }

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

                                {admin &&

                                    <span className="owner-tag">

                                        {

                                            task.owner === currentUserId

                                            ?

                                            "Owned by you"

                                            :

                                            `Owner: ${task.owner.slice(-6)}`

                                        }

                                    </span>

                                }

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