#!/usr/bin/env python3
"""Простой CLI-менеджер задач с сохранением в JSON."""

import json
import os
from datetime import datetime
from typing import List, Optional

DATA_FILE = os.path.expanduser("~/tasks.json")


class Task:
    def __init__(self, title: str, done: bool = False, created_at: Optional[str] = None):
        self.title = title
        self.done = done
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {"title": self.title, "done": self.done, "created_at": self.created_at}

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(title=data["title"], done=data["done"], created_at=data.get("created_at"))

    def __repr__(self) -> str:
        status = "✅" if self.done else "⬜"
        return f"{status} {self.title}"


class TaskManager:
    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = filepath
        self.tasks: List[Task] = []
        self.load()

    def load(self) -> None:
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]

    def save(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self.tasks], f, ensure_ascii=False, indent=2)

    def add(self, title: str) -> None:
        self.tasks.append(Task(title=title))
        self.save()
        print(f'Добавлена задача: "{title}"')

    def list(self, show_all: bool = True) -> None:
        if not self.tasks:
            print("Задач пока нет.")
            return
        for i, task in enumerate(self.tasks, start=1):
            if show_all or not task.done:
                print(f"{i}. {task}")

    def done(self, index: int) -> None:
        if not self._valid_index(index):
            return
        self.tasks[index - 1].done = True
        self.save()
        print(f'Задача "{self.tasks[index - 1].title}" выполнена!')

    def delete(self, index: int) -> None:
        if not self._valid_index(index):
            return
        removed = self.tasks.pop(index - 1)
        self.save()
        print(f'Удалена задача: "{removed.title}"')

    def _valid_index(self, index: int) -> bool:
        if index < 1 or index > len(self.tasks):
            print("Неверный номер задачи.")
            return False
        return True


def print_menu() -> None:
    print("\n=== Менеджер задач ===")
    print("1. Добавить задачу")
    print("2. Показать все задачи")
    print("3. Показать невыполненные")
    print("4. Отметить выполненной")
    print("5. Удалить задачу")
    print("0. Выход")


def main() -> None:
    manager = TaskManager()

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            title = input("Введите задачу: ").strip()
            if title:
                manager.add(title)
            else:
                print("Задача не может быть пустой.")
        elif choice == "2":
            manager.list(show_all=True)
        elif choice == "3":
            manager.list(show_all=False)
        elif choice == "4":
            try:
                index = int(input("Номер задачи: "))
                manager.done(index)
            except ValueError:
                print("Введите число.")
        elif choice == "5":
            try:
                index = int(input("Номер задачи: "))
                manager.delete(index)
            except ValueError:
                print("Введите число.")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
