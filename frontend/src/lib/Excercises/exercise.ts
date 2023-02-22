import type { languages, exercises } from "../constants";

interface ExerciseType {
  exercise_id: number,
  exercise_title: string,
  exercise_description: string,
  exercise_type_name: string,
  exercise_type_value: exercises,
  exercise_language_type: languages,
  exercise_language_name: string,
  exercise_content: object,
  exercise_solution: object
}

export interface ProgrammingExerciseType extends ExerciseType {
  exercise_content: {
    code: string;
    func: string;
  };
  exercise_solution: {
    key: [params: Array<number>, result: Array<number>];
  };
}

export interface ParsonsPuzzleExerciseType extends ExerciseType {
  exercise_content: {
    list: Array<string>;
  };
  exercise_solution: {
    list: Array<string>;
  };
}

// export interface FillInBlanksExerciseType extends ExerciseType {
//   exercise_content: {
//     text: String;
//     blankPos: Array<int>; // welcher integer?
//   };
//   exercise_solution: {
//     userEntries: Array<string>;
//   };
// }

export const getExercise = async (
  exerciseID: number
): Promise<ProgrammingExerciseType | ParsonsPuzzleExerciseType> => {
  try {
    const response = await fetch(
      `/exercise?exercise_id=${exerciseID}&exercise_limit=1&exercise_details=true`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }
    );
    if (!response.ok) {
      throw new Error();
    }
    return await response.json().then((data) => data.data[0]); // Last index should be exerciseID, not 0
  } catch (error) {
    throw new Error();
  }
};
