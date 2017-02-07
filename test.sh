osascript <<EOD
            tell application "Reminders"
                --set output to name of reminders
                set myList to "inbox - thespacedoctor"
                if (count of (reminders in list myList whose completed is false)) > 0 then
                    set todoListNames to name of reminders in list myList whose completed is false
                    set todoListNotes to body of reminders in list myList whose completed is false
                    set todoListDates to due date of reminders in list myList whose completed is false
                    set output to ""
                    repeat with itemNum from 1 to (count of todoListNames)
                        set output to output & "- " & (item itemNum of todoListNames)
                        if (item itemNum of todoListDates) > date "Tuesday, 25 December 1900 at 00:00:00" then
                            set dueDate to my date_time_to_iso(item itemNum of todoListDates)
                            set output to output & " @due(" & dueDate & ")"
                        end if
                        set output to output & "\n"
                        if item itemNum of todoListNotes exists then
                            repeat with para in every paragraph of (item itemNum of todoListNotes)
                                set output to (output & "    " & para as string) & "\n"
                            end repeat
                        end if
                    end repeat
                else
                    set output to ""
                end if

                return output
            end tell

            on date_time_to_iso(dt)
                set {year:y, month:m, day:d, hours:h, minutes:min, seconds:s} to dt
                set y to text 2 through -1 of ((y + 10000) as text)
                set m to text 2 through -1 of ((m + 100) as text)
                set d to text 2 through -1 of ((d + 100) as text)
                set h to text 2 through -1 of ((h + 100) as text)
                set min to text 2 through -1 of ((min + 100) as text)
                set s to text 2 through -1 of ((s + 100) as text)
                return y & "-" & m & "-" & d & " " & h & ":" & min
            end date_time_to_iso
EOD
