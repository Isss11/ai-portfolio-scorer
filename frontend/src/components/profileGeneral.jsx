const ProfileGeneral = ({ profile }) => {
    console.log({ profile })

    return (
        <li>
            <table>
                <tr>
                    <th></th>
                    <th>Readability</th>
                    <th>Best Practices</th>
                    <th>Maintainability</th>
                    <th>Impact</th>
                    <th>Experience</th>
                    <th>General</th>
                </tr>
                <tr>
                    <td>
                        <div>{profile.name}</div>
                        <div>{profile.username}</div>
                    </td>
                    <td>{profile.readability}</td>
                    <td>{profile.bestCodingPractices}</td>
                    <td>{profile.maintainability}</td>
                    <td>{profile.impact}</td>
                    <td>{profile.experience}</td>
                    <td>{profile.generalScore}</td>
                </tr>
            </table>
        </li>
    );
}

export default ProfileGeneral;